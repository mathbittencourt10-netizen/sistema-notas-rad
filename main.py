import sys
from views.login_view import LoginView


def main():
    app = LoginView()
    app.mainloop()


if __name__ == "__main__":
    main()
