# 🎂 SurpriseCraft: Premium Birthday Surprise Maker

SurpriseCraft is a highly interactive, beautifully animated, mobile-first web application designed to craft custom birthday surprises for your friends. Users can register, log in to a dashboard, configure custom birthday greetings, and generate shareable play links for their friends.

The player experience features sound effects synthesized via the browser's Web Audio API and highly engaging HTML5/CSS3 mini-games.

---

## ✨ Features

### 📂 Owner Dashboard (Creator Panel)
- **Secure Auth**: Creation of accounts and login using JWT tokens (reusing the authentication database layer of FastAPI).
- **Surprise Link Generator**: Input your friend's name and type a custom letter.
- **Manage Surprises**: View list of all active links, preview the surprise, copy the shareable URL, or delete expired surprises.

### 🎮 Surprise Player Flow (Recipient Panel)
- **Stage 1 (Welcome)**: Confetti showers with an interactive "Are you excited?" check. The **No** button playfully dodges tap and mouse hover events, making it impossible to choose anything but **Yes**!
- **Stage 2 (Balloon Pop)**: Clean glass-textured balloons float on screen. Popping all 4 bursts custom particle graphics and plays pop sounds, revealing the premium glowing text *"You are so special"*.
- **Stage 3 (Cake & Candle)**: Chocolate cake with dripping frosting and a flickering candle flame. Clicking the flame blows it out, rising a puff of smoke, and prompting a silent wish.
- **Stage 4 (Bouquet)**: Renders a professional, vibrant rose bouquet card with drifting rose petals.
- **Stage 5 (Tactile Letter)**: A closed pink and gold-rimmed envelope sealed with a red wax stamp. Tapping it cracks/shatters the seal, flips open the envelope in 3D space, and slides out your custom lined notebook letter.
- **Stage 6 (Final Screen)**: Adorable cartoon celebration greeting card, final wishes, and replay/create options.

---

## 🛠️ Tech Stack
- **Backend**: FastAPI (Python 3.13+)
- **Database**: SQLite (SQLAlchemy ORM)
- **Frontend**: HTML5, Vanilla JavaScript, CSS3 variables, transitions, and keyframe animations
- **Audio**: Web Audio API (Synthesized pop and whoosh sounds)
- **Fonts**: Outfit (Google Fonts UI) & Sacramento (handwritten cursive styles)

---

## ⚙️ Local Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/birthday_wishes_templeate.git
   cd birthday_wishes_templeate
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the local development server**:
   ```bash
   uvicorn main:app --reload
   ```
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser.

---

## 🚀 Deployment to Render

1. Create a new **Web Service** on Render and link your GitHub repository.
2. Select **Runtime**: `Python`
3. Configure the following build properties:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables if deploying with PostgreSQL (optional):
   - Key: `DATABASE_URL`
   - Value: `postgresql://...` (Render Database URL)
