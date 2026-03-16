# ... (الجزء العلوي من كودك يبقى كما هو بدون تغيير)

        # شروق وغروب الشمس - هذا هو الجزء الذي كان يحتوي على الخطأ في السطر 421
        col1, col2 = st.columns(2)
        with col1:
            # تم تصحيح السطر 421 هنا بإزالة الرمز المسبب للمشكلة
            st.markdown(f"""
                <div class="sun-card">
                    <div class="metric-label" style="color: white; opacity: 0.9;">الشروق</div>
                    <div class="metric-value" style="color: white;">{datetime.fromisoformat(daily['sunrise'][0]).strftime('%I:%M %p')}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="sun-card" style="background: linear-gradient(135deg, #2c3e50 0%, #4ca1af 100%);">
                    <div class="metric-label" style="color: white; opacity: 0.9;">الغروب</div>
                    <div class="metric-value" style="color: white;">{datetime.fromisoformat(daily['sunset'][0]).strftime('%I:%M %p')}</div>
                </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### 🗓️ توقعات الأيام السبعة القادمة")
        df_daily = pd.DataFrame({
            "التاريخ": [datetime.fromisoformat(t).strftime('%Y-%m-%d') for t in daily['time']],
            "الحرارة القصوى (°C)": daily['temperature_2m_max'],
            "الحرارة الدنيا (°C)": daily['temperature_2m_min'],
            "الأمطار (مم)": daily['precipitation_sum'],
            "مؤشر UV": daily['uv_index_max']
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_daily["التاريخ"], y=df_daily["الحرارة القصوى (°C)"], name="العظمى", line=dict(color='#ff4b4b', width=4)))
        fig.add_trace(go.Scatter(x=df_daily["التاريخ"], y=df_daily["الحرارة الدنيا (°C)"], name="الصغرى", line=dict(color='#1c83e1', width=4)))
        fig.update_layout(title="تذبذب درجات الحرارة خلال الأسبوع", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.table(df_daily)

    with tab3:
        st.markdown("### 🌡️ تفاصيل تقنية إضافية")
        c1, c2, c3 = st.columns(3)
        c1.metric("الرؤية", f"{current['visibility'] / 1000} كم")
        c2.metric("مؤشر UV اليوم", daily['uv_index_max'][0])
        c3.metric("كمية الأمطار المتوقعة", f"{daily['precipitation_sum'][0]} مم")

    with tab4:
        st.markdown("### 🎯 التوصيات")
        temp = current['temperature_2m']
        if temp > 30:
            st.warning("⚠️ الجو حار جداً")
        elif temp < 15:
            st.info("🧥 الجو بارد")
        else:
            st.success("🌤️ الجو مثالي")

else:
    st.info("💡 أدخل اسم مدينة في الشريط الجانبي لبدء عرض بيانات الطقس.")

st.markdown("---")
st.markdown("<center style='color: #666;'>تم التطوير بواسطة <b>طاهر</b> | 2026</center>", unsafe_allow_html=True)
