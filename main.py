import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://docs.google.com/forms/d/e/1FAIpQLSczCeN375TPVdT7XN4KfqicQMDo3KosTAROX75OJJ7GPsMGVQ/viewform")
    page.get_by_role("radio", name="นาย").click()
    page.get_by_role("textbox", name="ชื่อ คำถามที่ต้องตอบ").fill("เอกพงศ์")
    page.get_by_role("textbox", name="สกุล คำถามที่ต้องตอบ").fill("คงสวัสดิ์")
    page.get_by_role("textbox", name="Email คำถามที่ต้องตอบ").fill("ake@test.python.com")
    page.keyboard.press("Tab")
    for i in range(4):
        time.sleep(0.3)
        page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    time.sleep(0.3)
    page.get_by_role("checkbox", name="เคย", exact=True).click()
    page.get_by_role("textbox", name="ความคิดเห็น (จัดเต็มมาเลย...) คำถามที่ต้องตอบ").fill("เหนื่อยแล้วกาฟจาร")
    page.get_by_role("button", name="Submit").click()

    # กด ดูการตอบกลับก่อนหน้า
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="ดูการตอบกลับก่อนหน้า").click()
    page1 = page1_info.value

    # รอให้เนื้อหาบนหน้าเว็บโหลดเสร็จ
    page1.wait_for_selector('body')

    # ดึงข้อความทั้งหมดใน body
    body_text = page1.locator("body").inner_text()
    
    # ใช้ Regular Expression เพื่อค้นหาและดึงตัวเลขจากข้อความ
    # 're.search' จะหาข้อความที่ตรงกับรูปแบบที่กำหนด
    match = re.search(r'การตอบกลับ (\d+) รายการ', body_text)

    if match:
        # ดึงตัวเลขที่อยู่ภายในวงเล็บ (group 1)
        response_count = match.group(1)
        print(f"จำนวนคำตอบที่พบ: {response_count} ข้อ")
    else:
        print("ไม่พบข้อความ 'คำตอบ X ข้อ' บนหน้าเว็บ")

    # ---------------------
    time.sleep(30)
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
