import streamlit as st
from pdf2image import convert_from_bytes
from io import BytesIO
import zipfile

# 網頁設定
st.set_page_config(page_title="PDF 轉圖工具", page_icon="🖼️")
st.title("🖼️ PDF 一鍵轉高清圖片檔")
st.write("上傳 PDF 後，系統會自動拆分每一頁並打包成 ZIP 讓你下載。")

# 上傳元件
uploaded_file = st.file_uploader("選擇 PDF 檔案", type="pdf")

if uploaded_file:
    # 畫質設定
    dpi = st.select_slider("選擇輸出畫質 (DPI)", options=[100, 150, 200, 300], value=200)
    st.info(f"目前設定：{dpi} DPI (推薦 200 以上用於印刷或簡報)")

    if st.button("🚀 開始渲染並打包"):
        with st.spinner('正在逐頁渲染圖片，請稍候...'):
            try:
                # 1. 讀取 PDF 並轉為圖片
                images = convert_from_bytes(uploaded_file.read(), dpi=dpi)
                
                # 2. 建立 ZIP 記憶體緩衝區
                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
                    for i, img in enumerate(images):
                        # 將每一頁轉為 JPEG 二進制數據
                        img_io = BytesIO()
                        img.save(img_io, 'JPEG', quality=95)
                        # 命名規則：頁碼_原始檔名.jpg
                        img_filename = f"Page_{i+1:03d}_{uploaded_file.name.replace('.pdf', '')}.jpg"
                        zip_file.writestr(img_filename, img_io.getvalue())
                
                st.success(f"✅ 轉換成功！共計 {len(images)} 頁。")
                
                # 3. 下載按鈕
                st.download_button(
                    label="📥 下載圖片壓縮包 (ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name=f"{uploaded_file.name.replace('.pdf', '')}_Images.zip",
                    mime="application/zip"
                )
            except Exception as e:
                st.error(f"轉換出錯了：{str(e)}")

st.divider()
st.caption("本工具使用 Python pdf2image 渲染技術，不存儲任何用戶檔案。")
