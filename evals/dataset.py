"""Example dataset for evaluation."""

# Sample dataset for evaluation
HIPLAB_DATASET = [
    {
        "question": "HipLab là công ty hoạt động trong lĩnh vực gì?",
        "expected_answer": "HipLab là công ty TNHH phần mềm, cung cấp các giải pháp và dịch vụ công nghệ thông tin cho khách hàng trong và ngoài nước."
    },
    {
        "question": "Mô hình hoạt động của HipLab tương tự công ty nào?",
        "expected_answer": "HipLab hoạt động theo mô hình tương tự FPT Software."
    },
    {
        "question": "Thời gian làm việc chính thức của HipLab là như thế nào?",
        "expected_answer": "Thời gian làm việc từ thứ 2 đến thứ 6, từ 8h30 đến 17h30, nghỉ trưa từ 12h đến 13h."
    },
    {
        "question": "Nhân viên HipLab có bao nhiêu ngày nghỉ phép năm?",
        "expected_answer": "Nhân viên HipLab có 12 ngày nghỉ phép năm và có thể tăng theo thâm niên."
    },
    {
        "question": "HipLab có cho phép nghỉ không lương không?",
        "expected_answer": "HipLab cho phép nghỉ không lương nhưng cần có sự phê duyệt của quản lý trực tiếp."
    },
    {
        "question": "Quy định nghỉ thai sản cho lao động nữ tại HipLab là gì?",
        "expected_answer": "Lao động nữ được nghỉ thai sản 6 tháng theo quy định của pháp luật."
    },
    {
        "question": "Lao động nam được hưởng quyền lợi gì khi vợ sinh con?",
        "expected_answer": "Lao động nam được nghỉ khi vợ sinh con theo quy định của nhà nước."
    },
    {
        "question": "Những quyền lợi chính mà nhân viên HipLab được hưởng là gì?",
        "expected_answer": "Nhân viên được hưởng lương tháng 13, thưởng dự án, bảo hiểm xã hội, bảo hiểm y tế, bảo hiểm thất nghiệp, đào tạo nội bộ và các hoạt động team building."
    },
    {
        "question": "Nhân viên HipLab có được chia sẻ mã nguồn ra bên ngoài không?",
        "expected_answer": "Nhân viên không được phép chia sẻ mã nguồn và tài liệu nội bộ ra bên ngoài."
    },
    {
        "question": "Những thông tin nào được xem là thông tin cần bảo mật?",
        "expected_answer": "Mã nguồn, tài liệu nội bộ và dữ liệu khách hàng được xem là thông tin cần bảo mật."
    },
    {
        "question": "Nghỉ làm không phép sẽ bị xử lý như thế nào?",
        "expected_answer": "Nghỉ làm không phép sẽ bị trừ lương theo ngày công và có thể bị xử lý kỷ luật."
    },
    {
        "question": "Đi làm muộn hoặc về sớm nhiều lần có thể bị xử lý ra sao?",
        "expected_answer": "Đi làm muộn hoặc về sớm nhiều lần có thể bị nhắc nhở hoặc trừ thưởng."
    },
    {
        "question": "Vi phạm bảo mật thông tin có thể dẫn đến hậu quả gì?",
        "expected_answer": "Vi phạm bảo mật có thể bị xử lý kỷ luật, phạt tiền hoặc chấm dứt hợp đồng."
    },
    {
        "question": "HipLab có chính sách thưởng cổ phiếu cho nhân viên không?",
        "expected_answer": "Tài liệu nội bộ không đề cập đến chính sách thưởng cổ phiếu cho nhân viên."
    },
    {
        "question": "HipLab có cho phép làm việc 100% remote không?",
        "expected_answer": "Tài liệu chỉ đề cập làm việc từ xa theo quy định từng dự án, không nêu làm việc 100% remote."
    },
    {
        "question": "Nhân viên có thể sử dụng tài nguyên công ty cho mục đích cá nhân không?",
        "expected_answer": "Nhân viên không được sử dụng tài nguyên công ty cho mục đích cá nhân trái phép."
    },
    {
        "question": "Hậu quả của các hành vi gian lận hoặc phá hoại tài sản công ty là gì?",
        "expected_answer": "Hành vi gian lận, phá hoại tài sản sẽ bị xử lý bồi thường thiệt hại và áp dụng mức kỷ luật cao nhất."
    },
    {
        "question": "HipLab yêu cầu nhân viên điều gì khi làm việc với đồng nghiệp và khách hàng?",
        "expected_answer": "HipLab yêu cầu nhân viên phải tôn trọng đồng nghiệp và khách hàng, làm việc chuyên nghiệp, đúng cam kết, và không phân biệt đối xử."
    },
    {
        "question": "Quy định bảo mật thông tin của HipLab bao gồm những nội dung nào?",
        "expected_answer": "Quy định bảo mật cấm chia sẻ mã nguồn và tài liệu nội bộ ra ngoài, không sử dụng tài nguyên công ty cho mục đích cá nhân trái phép, vi phạm bảo mật có thể bị xử lý kỷ luật hoặc bồi thường thiệt hại."
    },
    {
        "question": "Những hình thức nghỉ nào được quy định trong chính sách nhân sự của HipLab?",
        "expected_answer": "HipLab quy định các hình thức nghỉ bao gồm: nghỉ phép năm (12 ngày/năm, tăng theo thâm niên), nghỉ ốm theo Luật Lao động, nghỉ việc riêng/hiếu hỉ (1-3 ngày), nghỉ thai sản (6 tháng cho lao động nữ), và nghỉ không lương (cần phê duyệt)."
    }
]



def get_evaluation_dataset():
    """Get evaluation dataset.
    
    Returns:
        List of evaluation examples
    """
    return HIPLAB_DATASET
