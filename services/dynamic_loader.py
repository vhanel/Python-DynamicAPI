from fastapi.routing import APIRoute
from controllers.dynamic_controller import create_dynamic_endpoint

async def reload_dynamic_routes(app, apis):
    # Remove rotas antigas da app
    app.router.routes = [
        route for route in app.router.routes
        if not (isinstance(route, APIRoute) and getattr(route, "is_dynamic", False))
    ]

    # Adiciona as novas
    for api in apis:
        endpoint = create_dynamic_endpoint(api.sql_query)
        route = APIRoute(
            path=api.endpoint,
            endpoint=endpoint,
            methods=["GET"],
            name=api.name,
            tags=[api.tag] if api.tag else ["Dynamic APIs"],
        )
        route.is_dynamic = True
        app.router.routes.append(route)

    # Atualiza o Swagger com as novas rotas
    app.openapi_schema = None  # força regeneração do Swagger
    app.openapi()