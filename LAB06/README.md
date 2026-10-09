# LAB06: RMUTT Planner

## ข้อมูลโปรเจกต์ (Project Info)
- **Main GitHub:** [https://github.com/Onpreyaq5/Nuthaluek-CPE-LLM-/tree/main/ProJ-RMUTT-Planner](https://github.com/Onpreyaq5/Nuthaluek-CPE-LLM-/tree/main/ProJ-RMUTT-Planner)
- **Fork GitHub:** [https://github.com/Automatic28m/ProJ-RMUTT-Planner-fork](https://github.com/Automatic28m/ProJ-RMUTT-Planner-fork)
- **Production App:** [https://rmutt-planner.noble-gold-society.workers.dev/](https://rmutt-planner.noble-gold-society.workers.dev/)

## รายละเอียดปัญหาและการแก้ไข (Project Details & Problem)
โปรเจกต์นี้เป็นโครงงานวิศวกรรมซอฟต์แวร์ (Software Engineering) แบบกลุ่มของมหาวิทยาลัย 

**ปัญหาที่พบ:** บัญชี GitHub ของเจ้าของโปรเจกต์หลัก (Onpreyaq5) ถูกระบบตรวจจับอัตโนมัติของ GitHub ระงับและขึ้นสถานะตรวจสอบบัญชี (Under Review) ส่งผลให้บัญชีและ Repository ทั้งหมดติดสถานะ **"Shadowban"** ซึ่งหมายความว่าเจ้าของบัญชียังสามารถล็อกอินและมองเห็นโค้ดของตัวเองได้ตามปกติ แต่หากเป็นบุคคลภายนอก เพื่อนร่วมกลุ่ม หรืออาจารย์ผู้สอนพยายามเข้าถึงลิงก์ จะแสดงหน้าจอ `404 Not Found` ทั้งหมด ทำให้ไม่สามารถเข้าถึงหรือ Clone โค้ดเพื่อนำไปให้คะแนนได้

**การแก้ไข:** เพื่อแก้ไขปัญหาเฉพาะหน้านี้ จึงได้ทำการ Fork/Clone โปรเจกต์ออกมายังบัญชีสำรอง (Automatic28m) ที่ยังใช้งานได้ปกติ และนำไปตั้งค่า Deploy ขึ้นระบบ Production ใหม่อีกครั้ง เพื่อให้อาจารย์สามารถเข้าถึงแอปพลิเคชันและตรวจให้คะแนนผลงานของกลุ่มได้สำเร็จ
