let route = window.location.pathname
route = route.replace('/', '')
dom = document.getElementById(route)
dom.classList.add('active')
