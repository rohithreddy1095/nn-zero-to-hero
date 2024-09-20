# Lyrikist - Lyrics Translator

Lyrikist is a web application that allows users to translate song lyrics into different languages with enhanced context and meaning using generative AI.

## Features

- Fetch lyrics of songs using the Musixmatch API.
- Translate lyrics into the target language using Google Translator.
- Enhance translated lyrics using OpenAI's GPT-3 to provide more meaningful and contextually appropriate translations.
- Display original and translated lyrics side by side.
- Provide additional track, artist, and album information.

## Prerequisites

- Python 3.x
- pip (Python package installer)
- Musixmatch API Key
- OpenAI API Key

## Installation

### Prerequisites

- Python 3.x
- pip package manager

### Setup Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/lyrikist.git
   cd lyrikist
   ```

2. **Create a virtual environment (optional)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API Keys**

   - Sign up for:
     - **Google Cloud Translation API** (or **DeepL API**).
     - **Musixmatch Lyrics API** (or **Genius API**).

   - Create a `.env` file in the project root:

     ```env
     GOOGLE_TRANSLATE_API_KEY=your_google_translate_api_key
     MUSIXMATCH_API_KEY=your_musixmatch_api_key
     OPENAI_API_KEY=your_openai_api_key
     ```

   Replace `your_google_translate_api_key`, `your_musixmatch_api_key`, and `your_openai_api_key` with your actual API keys.

5. **Run the application**

   ```bash
   python app.py
   ```

6. **Access the app**

   Open your browser and navigate to `http://localhost:5000`.

## Usage

- **By Song Name**: Enter the song name and artist name to fetch lyrics automatically.
- **By Lyrics**: Paste Punjabi lyrics directly to translate.

## Project Structure
    lyrikist/
    ├── app.py
    ├── .env
    ├── README.md
    ├── requirements.txt
    ├── static/
    │   └── styles.css
    └── templates/
        └── index.html

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
