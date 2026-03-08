# الحصول على الرد من جوجل
        response = model.generate_content(user_text)
        bot_reply = response.text
        st.success(f"🤖 المساعد: {bot_reply}")
        
        # نطق الرد
        tts = gTTS(text=bot_reply, lang='ar')
        # ... باقي الكود

