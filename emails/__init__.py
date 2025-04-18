import os

CLIENT_EMAIL = os.environ.get("CLIENT_EMAIL")
CLIENT_PASSWORD = os.environ.get("CLIENT_PASSWORD")

CUSTOMER_EMAIL_TEMPLATE = (
    message
) = """
    <div class="email" style="padding: 1em; background-color: white; border-radius: 20px; box-shadow: 5px 5px 5px #705503, -5px -5px 5px #494905">
  <p class="header" style="font-size: 2em; line-height: 1.1; color: #ed9b1f">
    <b>Thank you for Registering</b>
  </p>
  <p class="salutation">Dear {0},</p>
  <p class="body">
    Thank you for registering to attend our exhibition #{1}. <br />
    Your secret key is <b>{2}</b>. <br />
    This key will be activated after payment is received. <br />
    This key is only valid during the exhibition period and will be used to attend the exhibition you enrolled for, whenever it is still available.
  </p>
  <p>The next step is payment.</p> 
  <p>Thank you!</p>
  <center>
    
    <b>Umurage Art Hub</b><br />
    <em>Artistry Unleashed, Inspiration Unveiled.</em>
  </center>
</div>

"""


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
