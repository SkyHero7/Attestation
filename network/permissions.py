from rest_framework import permissions


class IsActiveEmployee(permissions.BasePermission):
    """
    Проверка активности пользователя.

    Позволяет доступ к представлению только активным и аутентифицированным пользователям.

    Методы:
        has_permission(request, view):
            Проверяет, имеет ли пользователь доступ к представлению на основе его аутентификации и активности.
    """

    def has_permission(self, request, view):
        """
        Проверяет, имеет ли пользователь доступ к представлению.

        Аргументы:
            request (Request): Объект запроса, содержащий информацию о пользователе.
            view (View): Представление, к которому осуществляется доступ.

        Возвращает:
            bool: True, если пользователь аутентифицирован и активен, иначе False.
        """
        return request.user and request.user.is_authenticated and request.user.is_active
