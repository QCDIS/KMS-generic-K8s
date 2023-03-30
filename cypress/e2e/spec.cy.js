describe.only('Test home page', () => {

  it('Reachability', () => {
    cy.visit('/')
  })

  it('Basic search from home page', () => {
    cy.visit('/')
    cy.get('#searchbox2').type('envri')
    cy.get('.search-btn').eq(1).click()
    cy.scrollTo('bottom')
    cy.get('.btn-primary').eq(1).click()
    cy.url().should('include', 'page=2')
    cy.scrollTo(0, 0)
  })

  it('Multiple search', () => {
    const search_urls = [
      'webSearch/genericsearch?page=1',
      'dataset_elastic/genericsearch?page=1',
      'webAPI/genericsearch?page=1',
      'notebookSearch/genericsearch?page=1',
      'webSearch/genericsearch?page=1&searchtype=imagesearch',
    ]
    for (const search_url of search_urls) {
      // Results everywhere
      cy.visit(`${search_url}&term=sea`)
      if (!search_url.includes('imagesearch')) {
        cy.contains(/I found (more than )?\d+ results for you!/)
      }
      // No results
      cy.visit(`${search_url}&term=n6lzhN2FB0rJkxsAH3NSH8aMW`)
      cy.contains(`I couldn't find anything based on "n6lzhN2FB0rJkxsAH3NSH8aMW" for you!`)
      // No results, search suggestion
      cy.visit(`${search_url}&term=gravitationnnally`)
      cy.contains(`I couldn't find anything based on "gravitationnnally" for you! Did you mean: gravitationally`)
    }
  })

  it('Nav bar buttons on home page', () => {
    cy.visit('/')
    // Shopping cart
    cy.contains('My Basket').should('not.be.visible')
    cy.get('.ti-shopping-cart').click()
    cy.contains('My Basket').should('be.visible')
    cy.get('.ti-shopping-cart').click()
    // Knowledge base links
    cy.contains('Ontowiki').should('not.be.visible')
    cy.contains('Knowledge Base').click()
    cy.contains('Ontowiki').should('be.visible')
    cy.contains('Knowledge Base').click()
  })

  it('Side bar buttons', () => {
    const search_urls = [
      `webSearch/genericsearch?page=1`,
      `dataset_elastic/genericsearch?page=1`,
      `webAPI/genericsearch?page=1`,
      `notebookSearch/genericsearch?page=1`,
      `webSearch/genericsearch?page=1&searchtype=imagesearch`,
    ]
    const menu_entries = [
      'Datasets',
      'Web APIs',
      'Notebooks',
      'Images',
      'Graph based',
      'Pie chart',
      'Publications',
      'R&D team',
    ]
    for (const search_url of search_urls) {
      cy.visit('/webSearch/genericsearch?term=envri&page=1')
      for (const menu_entry of menu_entries) {
        cy.contains(menu_entry).each(link => {
          if (link.prop('href'))
            cy.request({
              url: link.prop('href'),
            })
          cy.log( link.prop('href'))
        })
      }
    }
  })

  it('Shopping cart behaviour', () => {
    let term = 'sea'
    const search_urls = [
      `webSearch/genericsearch?page=1&term=${term}`,
      `dataset_elastic/genericsearch?page=1&term=${term}`,
      `webAPI/genericsearch?page=1&term=${term}`,
      `notebookSearch/genericsearch?page=1&term=${term}`,
      `webSearch/genericsearch?page=1&searchtype=imagesearch&term=${term}`,
    ]
    // Check initial cart count
    for (const search_url of search_urls) {
      cy.visit(search_url)
      cy.get('#MyCartCount').contains(/^0$/)
    }
    // Add item to cart
    cy.visit(search_urls[0])
    cy.get('.breadcrumb-item > a').eq(1).find('img[src*="addToBasket.png"]').click()
    // Check updated cart count
    for (const search_url of search_urls) {
      cy.visit(search_url)
      cy.get('#MyCartCount').contains(/^1$/)
    }
  })

})