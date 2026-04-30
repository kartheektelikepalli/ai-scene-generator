import warnings

# Suppress SSL warning
warnings.filterwarnings("ignore")

from app.main import run

if __name__ == "__main__":
    run()