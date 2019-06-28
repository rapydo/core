it('login', () => {
  cy.visit('/')

  cy.get('[routerlink="/app/login"]').click()

  cy.get('#formly_1_input_username_0')
    .type(Cypress.env('USERNAME'))

  cy.get('#formly_1_input_password_1')
    .type(Cypress.env('PASSWORD'))

  cy.get('form').submit()

  cy.wait(2000)

  cy.visit('/app/profile')

  cy.contains('.card-header h4', /User profile/)

  cy.wait(1000)
})
