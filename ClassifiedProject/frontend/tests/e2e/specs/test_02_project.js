// https://docs.cypress.io/api/table-of-contents

describe("test project manage", () => {
  it("login", () => {
    cy.visit("/");
    cy.get("[cy-data=LoginUsername]", { timeout: 3000 }).clear();
    cy.get("[cy-data=LoginUsername]", { timeout: 3000 }).type("hxh");
    cy.get("[cy-data=LoginPassword]", { timeout: 3000 }).clear();
    cy.get("[cy-data=LoginPassword]", { timeout: 3000 }).type("abc123");
    cy.get("[cy-data=loginButton]", { timeout: 3000 }).click();
    cy.contains("[cy-data=loginSuccess]", "欢迎");
  });
  it("create", () => {
    cy.visit("/main/project");
    var timestamp = Date.parse(new Date());
    cy.get("[cy-data=ProjectCreate]", { timeout: 3000 }).click();
    cy.get("[cy-data=ProjectName]", { timeout: 3000 }).type(
      "项目" + timestamp.toString()
    );
    cy.get("[cy-data=ProjecDescribe]", { timeout: 3000 }).type("项目描述");
    cy.get("[cy-data=ProjectOk]", { timeout: 3000 }).click();
  });
  it("edit", () => {
    cy.visit("/main/project");
    var timestamp = Date.parse(new Date());
    cy.get("[cy-data=ProjectSetting]", { timeout: 3000 })
      .eq(1)
      .click({ force: true });
    cy.get("[cy-data=ProjectEdit]", { timeout: 3000 })
      .eq(1)
      .click({ force: true });
    cy.get("[cy-data=ProjectName]", { timeout: 3000 }).type(
      "项目" + timestamp.toString()
    );
    cy.get("[cy-data=ProjecDescribe]", { timeout: 3000 }).type("项目描述");
    cy.get("[cy-data=ProjectOk]", { timeout: 3000 }).click();
  });
  it("edit", () => {
    cy.visit("/main/project");
    cy.get("[cy-data=ProjectSetting]", { timeout: 3000 })
      .eq(-1)
      .click({ force: true });
    cy.get("[cy-data=ProjectDelete]", { timeout: 3000 })
      .eq(1)
      .click({ force: true });
    cy.contains("p", "删除成功");
  });
  it("list page", () => {
    cy.visit("/main/project");
    cy.get("[cy-data=ProjectPagination] > ul.el-pager > li.number", {
      timeout: 3000,
    })
      .eq(1)
      .click();
    cy.get("[cy-data=ProjectPagination] > button.btn-next", {
      timeout: 3000,
    }).click();
  });
});
