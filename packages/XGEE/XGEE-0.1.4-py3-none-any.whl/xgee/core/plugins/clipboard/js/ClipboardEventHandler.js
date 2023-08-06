(function _registerHotkeys(){
    var eventBroker=$app.plugins.require('eventBroker');

    document.addEventListener('paste', (event) => {
        eventBroker.publish('CLIPBOARD/CMD/PASTE',{evt:event, dat: null});    
        event.preventDefault();
    });

    document.addEventListener('cut', (event) => {     
        eventBroker.publish('CLIPBOARD/CMD/CUT',{evt:event, dat: null});    
        event.preventDefault();
    });

    document.addEventListener('copy', (event) => {     
        eventBroker.publish('CLIPBOARD/CMD/COPY',{evt:event, dat: null});    
        event.preventDefault();
    });
    

})();