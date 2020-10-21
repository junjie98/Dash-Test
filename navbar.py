import dash_bootstrap_components as dbc


def Navbar():
    """This is the Navigation Bar"""
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("View Dataset", href="/viewDataset")),
            dbc.NavItem(dbc.NavLink("Predictor", href="/predictor")),
        ],
        brand="Home",
        brand_href="/",
        color="dark",
        dark=True,
        className="pb-1",
    )
    return navbar
