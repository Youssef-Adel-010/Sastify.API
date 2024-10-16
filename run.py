from app import create_app;

def main():
    app = create_app()
    
    if __name__ == '__main__':
        app.run()

main()