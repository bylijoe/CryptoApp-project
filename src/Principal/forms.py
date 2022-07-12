from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms import HiddenField, SubmitField,FloatField
from wtforms.validators import DataRequired

class PurchaseForm(FlaskForm):
   
    cryptomonedas=[("EUR","Euro"),("BTC","Bitcoin"),("ETH","Ether"),("USDT","Tether"),("ADA","Cardano"),
                   ("SOL","Solana"),("XRP","Ripple"), ("DOT","Polkadot"),("DOGE","Dogecoin"),("SHIB","Shibs_Inu")]

    id =HiddenField()
    from_currency = SelectField( "From:",
                             validators=[DataRequired(message="Seleccione la moneda a cambiar")],choices =cryptomonedas )
    from_quantity= FloatField ("Q:", validators=[DataRequired(message="Debes indicar una cantidad")])
    to_currency= SelectField("To:",
                             validators=[DataRequired(message="Seleccione la moneda a devolver")],choices = cryptomonedas )
    to_quantity=FloatField("Q:" )

    P_U=FloatField("P.U.:")

    submit_calcular=SubmitField("Calcular")
    submit_aceptar= SubmitField("Aceptar")