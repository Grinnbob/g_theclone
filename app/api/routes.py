from .endpoints import users, accounts, lists, forms, addons, admin

def setup_routes(app):
    app.include_router(
        users.router,
        prefix="/users"
    )
    app.include_router(
        accounts.router,
        prefix="/accounts"
    )
    app.include_router(
        lists.router,
        prefix="/lists"
    )
    app.include_router(
        forms.router,
        prefix="/forms"
    )
    app.include_router(
        addons.router,
        prefix="/addons"
    )
    app.include_router(
        admin.router,
        prefix="/admin"
    )
