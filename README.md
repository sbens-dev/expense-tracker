# 💳 Personal Expense Tracker

A simple, beginner-friendly web application to record your daily purchases, pick categories (like Food or Gas), and see your weekly spending at a glance.

Designed to work cleanly on **both smartphones and computers**, keeping your data synced in real time.

---

## ✨ Features
- **Quick Entry:** Type the dollar amount, a short note (e.g., "Coffee"), pick a category, and save in seconds.
- **Pre-Made Categories:** `Food`, `Gas`, `Groceries`, `Bills`, `Entertainment`, `Shopping`, and `Other`.
- **Weekly Dashboard:** Prominently shows your grand total spent this week (Sunday to Saturday) and a breakdown by category.
- **Instant Sync:** Save on your phone while out shopping; see it waiting on your computer when you get home.
- **Local Preview Mode:** Works immediately right out of the box with temporary memory—even before setting up an online account.

---

## 🚀 Quickstart: Run the App on Your Computer

1. Open your terminal in this folder and make sure helper tools are installed:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the app:
   ```bash
   streamlit run src/app.py
   ```
3. Open the link shown in your terminal (usually **`http://localhost:8501`**) in your web browser!

---

## ☁️ Step-by-Step: Connect Your Free Supabase Database (Phone Sync)

To keep your phone and computer in sync, you need a free online "filing cabinet" provided by **Supabase**. Here are the simple steps to set it up:

### Step 1: Create Your Free Supabase Account
1. Visit [https://supabase.com](https://supabase.com) and click **Sign Up** (it's 100% free).
2. Click **New Project**.
3. Give your project a friendly name (e.g. `My Expense Tracker`) and set a database password you'll remember.
4. Click **Create new project** and wait about 1 minute for it to finish setting up.

### Step 2: Create the `expenses` Table
1. In your Supabase project dashboard, click on **SQL Editor** in the left sidebar (it looks like a small terminal `>_` icon).
2. Click **New Query**.
3. Paste the following 5 lines of setup text into the box:
   ```sql
   CREATE TABLE expenses (
     id BIGSERIAL PRIMARY KEY,
     created_at TIMESTAMPTZ DEFAULT NOW(),
     amount NUMERIC(10, 2) NOT NULL,
     category TEXT NOT NULL,
     description TEXT,
     date DATE NOT NULL
   );
   ```
4. Click the green **Run** button. You'll see a *"Success. No rows returned"* message. Your online filing cabinet is ready!

### Step 3: Copy Your Secret Connection Keys
1. In the left sidebar of Supabase, click the **Settings** gear icon at the bottom, then click **API**.
2. Find:
   - **Project URL** (looks like: `https://abcdefghijkl.supabase.co`)
   - **Project API Keys** -> find the key labeled **`anon` `public`** (a long string of random letters and numbers).

### Step 4: Paste Keys into Your App
1. In your project's `.streamlit` folder, duplicate the file named `secrets.toml.example` and name the new file **`secrets.toml`**:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```
2. Open `.streamlit/secrets.toml` in your text editor and paste your real URL and key:
   ```toml
   [supabase]
   url = "https://your-project-id.supabase.co"
   key = "your-actual-anon-key-here"
   ```
3. Save the file.
4. Refresh your browser at `http://localhost:8501`. You will see the green **🟢 Cloud Sync Active** banner! Anything you type will now be safely saved online.

---

## 📱 How to Open the App on Your Phone

### Option A: On Your Home Wi-Fi (Instant)
When you run `streamlit run src/app.py`, your terminal displays two addresses:
```text
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```
As long as your phone is connected to the same Wi-Fi network as your computer, simply type that **Network URL** into Safari or Chrome on your phone. You can bookmark it or tap **Add to Home Screen** to use it like a native phone app!

### Option B: Free Cloud Hosting (Accessible Anywhere in the World)
If you want to use the app when you are away from home on cellular data:
1. Push this project to a free GitHub repository.
2. Go to [https://share.streamlit.io](https://share.streamlit.io) (free Streamlit Community Cloud).
3. Connect your GitHub repository and select `src/app.py`.
4. In the Streamlit Cloud dashboard, click **Settings > Secrets** and paste the same contents of your `secrets.toml`.
5. Streamlit will give you a public web link (like `https://my-expenses.streamlit.app`) that you can open on any phone anywhere!

---

## 🧪 Running Automated Tests

To verify that all math, weekly date logic, and database safeguards work properly:
```bash
pytest
```
Expected output:
```text
============================== 18 passed in 1.38s ==============================
```

---

## 📂 Project Organization

```text
expense-tracker/
├── .streamlit/
│   ├── secrets.toml.example  # Template with instructions on connecting Supabase
│   └── secrets.toml          # Your private keys (ignored by git for security)
├── src/
│   ├── app.py                # Main visual application (Streamlit screens & buttons)
│   ├── calculations.py       # Calculator brain (Sunday-to-Saturday math & category totals)
│   └── database.py           # Online filing cabinet connector (Supabase save/load)
├── tests/
│   ├── test_calculations.py  # Tests for spending math and week date boundaries
│   ├── test_database.py      # Tests for database validation and cloud fallbacks
│   └── test_app.py           # Tests verifying the visual app runs cleanly
├── .gitignore                # Protects your private keys from being shared
├── requirements.txt          # Tools needed to run the app
├── SPEC.md                   # The official blueprint
└── README.md                 # This beginner-friendly user guide
```
