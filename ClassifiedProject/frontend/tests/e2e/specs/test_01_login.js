// https://docs.cypress.io/api/table-of-contents

describe("login", () => {
  it("home", () => {
    cy.visit("/");
    cy.contains("接口测试平台");
  });
  it("login", () => {
    cy.visit("/");
    cy.get("[cy-data=LoginUsername]", { timeout: 3000 }).clear();
    cy.get("[cy-data=LoginUsername]", { timeout: 3000 }).type("hxh");
    cy.get("[cy-data=LoginPassword]", { timeout: 3000 }).clear();
    cy.get("[cy-data=LoginPassword]", { timeout: 3000 }).type("abc123");
    cy.get("[cy-data=loginButton]", { timeout: 3000 }).click();
    cy.contains("[cy-data=loginSuccess]", "欢迎");
  });
});
