<style>
    /* خلفية الموقع كاملة بصورة سحابية ناعمة */
    .stApp {
        background: url('https://images.unsplash.com/photo-1513002749550-c59d786b8e6c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-attachment: fixed;
    }

    /* تصميم البطاقة الزجاجية */
    .smart-card, .main-header, .stTabs, [data-baseweb="tab-panel"] {
        background: rgba(255, 255, 255, 0.15) !important; /* شفافية زجاجية */
        backdrop-filter: blur(15px) !important; /* تأثير الضباب */
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2) !important; /* حدود زجاجية */
        border-radius: 25px !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15) !important;
        color: white !important;
    }

    /* تحسين النصوص لتظهر بوضوح فوق الزجاج */
    h1, h2, h3, p, .metric-value, .sub-info {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }

    /* جعل التبويبات (Tabs) زجاجية أيضاً */
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px;
        color: white !important;
        margin-right: 5px;
    }
</style>
