import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load token from environment variable
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Yamnitsa coordinates
LAT = 48.9344
LON = 24.7701
SYSTEM_CAPACITY_KW = 5
EFFICIENCY = 0.8

def calculate_pv_generation(irradiation_kwh_m2):
    return irradiation_kwh_m2 * SYSTEM_CAPACITY_KW * EFFICIENCY

def get_tomorrow_irradiation():
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}"
        "&daily=shortwave_radiation_sum&timezone=auto"
    )
    response = requests.get(url)
    data = response.json()
    irradiation = data["daily"]["shortwave_radiation_sum"][1]
    date = data["daily"]["time"][1]
    return irradiation, date

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    irradiation, date = get_tomorrow_irradiation()
    predicted_generation = calculate_pv_generation(irradiation)
    msg = (
        f"🌞 Solar Prediction for {date}:\n"
        f"🔆 Irradiation: {irradiation:.2f} kWh/m²\n"
        f"⚡ Estimated PV Output: {predicted_generation:.2f} kWh"
    )
    await update.message.reply_text(msg)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("predict", predict))
    print("Bot is running...")
    app.run_polling()
