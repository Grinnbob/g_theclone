from . import get_stream_app, init_processors



if __name__ == '__main__':
    app = get_stream_app()

    app.main()