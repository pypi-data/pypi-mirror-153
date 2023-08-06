import streamlit as st

from lumipy.atlas.utility_functions import (
    _query_data_provider_metadata,
    _query_direct_provider_metadata,
    _build_data_provider_factories,
    _build_direct_provider_factories
)
from lumipy.atlas.atlas import Atlas
from lumipy.client import Client

from typing import Optional, NoReturn

from lumipy.common.string_utils import random_globe
from lumipy.streamlit.reporter import Reporter
from lumipy.query.expression.table_op.base_table_op import BaseTableExpression
from pandas import DataFrame


def get_atlas(container, **kwargs) -> Atlas:
    """Get luminesce data provider atlas instance.

    Args:
        container: streamlit container to display running query information in.

    Keyword Args:
        token (str): Bearer token used to initialise the API
        api_secrets_filename (str): Name of secrets file (including full path)
        api_url (str): luminesce API url
        app_name (str): Application name (optional)
        certificate_filename (str): Name of the certificate file (.pem, .cer or .crt)
        proxy_url (str): The url of the proxy to use including the port e.g. http://myproxy.com:8888
        proxy_username (str): The username for the proxy to use
        proxy_password (str): The password for the proxy to use
        correlation_id (str): Correlation id for all calls made from the returned finbournesdkclient API instances

    Returns:
        Atlas: the atlas instance.

    """
    log = container.empty()

    report = Reporter(log)

    client = Client(**kwargs)

    def _print(x, end='\n'):
        report.update(x + end)

    # Note: can't store the atlas itself because object isinstance checks fail between runtimes
    # This leads to type checking failing when you use fluent syntax from an atlas generated in a different runtime.
    # We have to store the data it's built from and rebuild from that. Thankfully the querying is the slow bit.

    if 'atlas_dfs' not in st.session_state:
        _print(f"Getting atlas{random_globe()}")
        _print("  • Querying data provider metadata...")
        data_df = _query_data_provider_metadata(client)

        _print("  • Querying direct provider metadata...")
        direct_df = _query_direct_provider_metadata(client)

        st.session_state['atlas_dfs'] = (data_df, direct_df)

    data_df, direct_df = st.session_state['atlas_dfs']
    data_provider_factories = _build_data_provider_factories(data_df, client)
    direct_provider_factories = _build_direct_provider_factories(direct_df, client)

    atlas = Atlas(
        data_provider_factories + direct_provider_factories,
        atlas_type='All available data providers'
    )

    report.empty()

    return atlas


def run_and_report(container, query: BaseTableExpression) -> DataFrame:
    """Runs lumipy query and publishes the progress information to a given container in your streamlit app. Also
    implements a cancel button that will stop the monitoring process and delete the running query.

    Args:
        query (BaseTableExpression): lumipy query expression object to run.
        container: streamlit container to display running query information in.

    Returns:
        DataFrame: dataframe containing the result of the query.
    """

    title = container.empty()
    cancel = container.empty()
    log = container.empty()

    report = Reporter(log)

    title.subheader('[lumipy] executing query')

    job = query.go_async(_print_fn=lambda x: report.update(x + '\n'))

    stop = cancel.button(key=job.ex_id, label='Cancel Query', on_click=job.delete)

    job.live_status(stop_trigger=lambda: stop)

    if stop:
        report.empty()
        cancel.empty()
        title.empty()
        return DataFrame()

    report.update("\n\nFetching results... ")
    df = job.get_result()
    report.update("done!\n")

    report.empty()
    cancel.empty()
    title.empty()

    return df


def use_full_width() -> NoReturn:
    """Make streamlit use the full width of the screen.

    Use by calling this function at the top of your application.

    """

    max_width_str = f"max-width: 2000px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )
