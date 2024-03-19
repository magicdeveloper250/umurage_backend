import os

CLIENT_EMAIL = os.environ.get("CLIENT_EMAIL")
CLIENT_PASSWORD = os.environ.get("CLIENT_PASSWORD")

CUSTOMER_EMAIL_TEMPLATE = (
    message
) = """
    <div class="email">
      <p class="header"><b>Registration message</b></p>
      <p class="salutation">Dear customer,</p>
      <p class="body">
        Thank you for making registration to attend our exhibition
        #{0}. <br />
        Your secret key is <b>{1}</b>. <br />
        This key will be activated after payment. <br />
        This key will only be valid during exhibition period and will be used to
        attend exhibition, you enrolled for; whenever is still available
      </p>
      <p>Thank you!</p>
      <p class="signature">
        <b>Umurage art hub</b><br />
        <em>Artistry unleashed, Insipiration unveiled.</em>
      </p>
      
    </div>"""
VERIFICATION_EMAIL_TEMPLATE = """
    <div class="email">
      <p class="header"><b>Registration message</b></p>
      <p class="salutation">Dear painter,</p>
      <p class="body">
        Thank you for creating an account.<br />
        Please click on the link below to verify your account.
        <a href="{0}"> <button> Verify</button></a>
      </p>
      <p>Thank you!</p>
      <p class="signature">
        <b>Umurage art hub</b><br />
        <em>Artistry unleashed, Insipiration unveiled.</em>
      </p>
      
    </div>"""
