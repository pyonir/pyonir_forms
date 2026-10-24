id: art_lovers
action: /api/demo-form-handler
method: POST
inputs:-
    label: *Email
    type: email
    placeholder: PabloPycasso@pyonir.dev
    required: true
    disabled: true
    -
    label: Subscriptions
    type: checkbox
    inputs:-
        Beyonce
        Masego
        WuTang
    -
    label: Sign In
    type: submit
    class: btn
````html js
art_lovers.addEventListener('change', (e)=>{
    console.log(e.target)
})
````
@response.message: Thank you for subscribing your {email} to {subscriptions}!
