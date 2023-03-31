    // get search form an dpage links
    let searchForm = document.getElementById('searchForm');
    let pageLinks = document.getElementsByClassName('page-link')


    // ensure searchForm exists
    if(searchForm){
        for(let i = 0; pageLinks.length > i; i++){
            pageLinks[i].addEventListener('click', function (e) {
                e.preventDefault();
                
                // get data attribute
                let page = this.dataset.page
                console.log('PAGE: ', page)

                // add hidden search input to form
                searchForm.innerHTML += `<input value=${page} name="page" hidden />`
                
                // submit invisible form
                searchForm.submit()
            })
        }
    }
