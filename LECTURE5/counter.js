
// Local storage
if (!localStorage.getItem('counter')) {
    localStorage.setItem('counter', 0);
}
let counter = 0;

function count(){

    // get the value of the counter from local storage.
    let counter = localStorage.getItem('counter');
    
    // increment by +1.
    counter++;
    
    // update by setting the value to be the counter.
    document.querySelector('h1').innerHTML = counter;
    
    // write to local storage.
    localStorage.setItem('counter', counter);

    /*
    if (counter % 10 === 0) {
        alert(`Count is now ${counter}`);
    }
    */

}

// 'DOMContentLoaded' waits until all the content has been loaded.
document.addEventListener('DOMContentLoaded', function() {
    
    // when page is loaded/refreshed, set the initial value of the innerHTML to be whatever localStorage has.
    document.querySelector('h1').innerHTML = localStorage.getItem('counter');
    
    document.querySelector('button').onclick = count;
    
    /* Demo: interval
    // Every so often, run a particular function; setInterval() is a built-in function.
    setInterval(count, 1000);
    */
});

/* Demo
// The following syntax would have worked the same as the above:
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('button').addEventListener('click', count);
});
*/