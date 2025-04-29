import json
import os

class Student:
    def __init__(self, name, mssv, student_class, phone, birthday, current_address):
        self.name = name
        self.mssv = mssv
        self.student_class = student_class
        self.phone = phone
        self.birthday = birthday
        self.current_address = current_address

    def to_dict(self):
        return {
            "Họ tên": self.name,
            "MSSV": self.mssv,
            "Lớp": self.student_class,
            "SĐT": self.phone,
            "Ngày sinh": self.birthday,
            "Địa chỉ hiện tại": self.current_address
        }

class Family(Student):
    def __init__(self, name, mssv, student_class, phone, birthday, current_address,
                 home_address, father_name, mother_name):
        super().__init__(name, mssv, student_class, phone, birthday, current_address)
        self.home_address = home_address
        self.father_name = father_name
        self.mother_name = mother_name

    def to_dict(self):
        return {
            "Thông tin sinh viên": super().to_dict(),
            "Thông tin gia đình": {
                "Địa chỉ gia đình": self.home_address,
                "Họ tên bố": self.father_name,
                "Họ tên mẹ": self.mother_name
            }
        }

class Manager:
    def __init__(self):
        self.students = []
        self.filename = "students.json"
        self.load_data()

    def add_student(self, student):
        self.students.append({
            "id": len(self.students) + 1,
            **student.to_dict()
        })
        self.save_data()

    def update_student(self, student_id, new_data):
        for student in self.students:
            if student["id"] == student_id:
                student.update(new_data)
                self.save_data()
                return True
        return False

    def delete_student(self, student_id):
        self.students = [s for s in self.students if s["id"] != student_id]
        self.save_data()

    def list_students(self):
        for student in self.students:
            print(json.dumps(student, indent=4, ensure_ascii=False))

    def save_data(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.students, f, indent=4, ensure_ascii=False)

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                self.students = json.load(f)

# ===== MAIN CLI MENU =====

if __name__ == "__main__":
    manager = Manager()

    while True:
        print("\n===== MENU =====")
        print("1. Thêm sinh viên")
        print("2. Cập nhật sinh viên")
        print("3. Xóa sinh viên")
        print("4. Hiển thị danh sách")
        print("5. Thoát")

        choice = input("Chọn: ")

        if choice == "1":
            name = input("Họ tên: ")
            mssv = input("MSSV: ")
            student_class = input("Lớp: ")
            phone = input("SĐT: ")
            birthday = input("Ngày sinh: ")
            current_address = input("Địa chỉ hiện tại: ")
            home_address = input("Địa chỉ gia đình: ")
            father_name = input("Họ tên bố: ")
            mother_name = input("Họ tên mẹ: ")

            sv = Family(name, mssv, student_class, phone, birthday, current_address,
                        home_address, father_name, mother_name)
            manager.add_student(sv)
            print("✅ Đã thêm!")

        elif choice == "2":
            sid = int(input("Nhập ID sinh viên cần cập nhật: "))
            field = input("Nhập trường cần sửa (ví dụ: Thông tin sinh viên -> SĐT): ")
            new_value = input("Giá trị mới: ")

            updated = False
            for student in manager.students:
                if student["id"] == sid:
                    # Cho phép cập nhật sâu
                    if "->" in field:
                        keys = field.split("->")
                        keys = [k.strip() for k in keys]
                        data = student
                        for k in keys[:-1]:
                            data = data.get(k, {})
                        data[keys[-1]] = new_value
                    else:
                        student[field] = new_value
                    updated = True
                    manager.save_data()
                    print("✅ Đã cập nhật.")
                    break
            if not updated:
                print("❌ Không tìm thấy sinh viên.")

        elif choice == "3":
            sid = int(input("Nhập ID sinh viên cần xóa: "))
            manager.delete_student(sid)
            print("🗑️ Đã xóa!")

        elif choice == "4":
            print("\n📋 Danh sách sinh viên:")
            manager.list_students()

        elif choice == "5":
            print("👋 Thoát chương trình.")
            break

        else:
            print("❌ Lựa chọn không hợp lệ.")
