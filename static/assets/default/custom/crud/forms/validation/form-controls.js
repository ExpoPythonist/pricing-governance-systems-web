let FormControls = {
    init: function () {
        $("#m_form_1").validate({
            rules: {
                email: {required: !0, email: !0, minlength: 10},
                username: {required: !0, minlength: 4},
                password: {required: !0, minlength: 6, maxlength: 14},
                confirm_password: {required: !0, equalTo: "#password"},
                user_type: {required: !0},
            }, invalidHandler: function (e, r) {
                $("#m_form_1_msg").removeClass("m--hide").show(), mUtil.scrollTop()
            }, submitHandler: function (e) {
                return true;
            }
        })
    },
    upload_profile_photo: () => {
        let profile_img = document.getElementById('profile_img');
        if (profile_img) {
            profile_img.addEventListener('change', (el) => {
                if (el.target.files && el.target.files) {
                    let reader = new FileReader();
                    reader.onload = (e) => {
                        $('#base64_user_img').val(e.target.result);
                    };
                    reader.readAsDataURL(el.target.files[0]);
                }
            })
        }

    }
};
jQuery(document).ready(function () {
    FormControls.init();
    FormControls.upload_profile_photo();
});