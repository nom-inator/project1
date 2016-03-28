function handleScroll()
{
    if(window.XMLHttpRequest)
    {
        var offset = window.pageYOffset
               ? window.pageYOffset
               : document.documentElement.scrollTop;

        document.getElementById('navigation').className =
            (offset > window.innerHeight ? 'fixed' : '');
    }
}

if(window.addEventListener)
{
    window.addEventListener('scroll', handleScroll, false);
}
else
{
    window.attachEvent('onscroll', handleScroll);
}