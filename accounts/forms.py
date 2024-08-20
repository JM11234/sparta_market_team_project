from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.urls import reverse


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number', 'birth_date', 'address')
        
        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.fields['address'].required = True    ## HTML에서 required를 통해서 유효성검사를 해도 우회할수있기때문에 내부적으로도 확인할수 있음


class CustomUserChangeForm(UserChangeForm):
    # password = None
    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.fields.get("password"):
            password_help_text = (
                "비밀번호를 변경할수 있습니다." '<a href = "{}">Here</a>'
            ).format(f"{reverse('accounts:change_password')}")
            self.fields["password"].help_text = password_help_text
