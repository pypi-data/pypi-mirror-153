// 2020 Bjoern Annighoefer

var NOTES_TOOL = NOTES_TOOL || {};

Object.assign(NOTES_TOOL,(function(){

    function NotesTool(params={},createDom=true) {
        jsa.Tool.call(this,params,false);
        jsa.Observer.call(this);
        
        //parameters
        this.app = null;
        this.notesManager = null;
        this.containerStyle = ['jsa-tool-container','tool-notes'];
        this.onClickCallback = function (e) {
            this.newNotes = false;
            this.UpdateLabel();
            this.ShowNotesList();
        };
        this.onNotifyCallback = function(event) {
            if(jsa.EVENT.IS_INSTANCE(event,jsa.EVENT.EVENT_ID([jsa.EVENT.TYPES.ADD,'notes']))) {
            // if(event.eventId == 'NEW') {
                this.newNotes = true;
                this.UpdateLabel();
                let note = event.value;
                if(this.shownNotes) {
                    this.AddNote(note);
                } else {
                    this.RebuildNotesList();
                }
                $.notify(note.message,note.level);
            } else if(jsa.EVENT.IS_INSTANCE(event,jsa.EVENT.EVENT_ID([jsa.EVENT.TYPES.METHOD_CALL,'ClearNotes']))) {    
            // } else if(event.eventId == 'CLEAR') {
                this.newNotes = false;
                this.UpdateLabel();
                this.RebuildNotesList();
            }
        }

        jsa.CopyParams(this,params);

        //internals
        this.infoBubble = null;
        this.newNotes = false;
        this.shownNotes = 0;

        //start listen to Events
        //make the domain status tool listen to the domain statistics
        if(this.notesManager) {
            this.notesManager.StartObserving(this);
        }

        if(createDom) {
            this.CreateDom();
        }

        //start listen to notes
        

        return this;
    }

    NotesTool.prototype = Object.create(jsa.Tool.prototype);
    jsa.Mixin(NotesTool,jsa.Observer);

    NotesTool.prototype.ShowNotesList = function() {
        //let app = this.GetApp();
        if(this.app) {
            if(!this.infoBubble) {
                this.infoBubble = new jsa.Bubble({
                    name: '',
                    startEnabled: true,
                    isResizable: false,
                    content: '',
                    isMinimizable: false, 
                    autoHide: true,
                    isClosable: false,
                    borderOffset: 25, //px
                    penaltyN: 0,
                    penaltyE: 2000,
                    penaltyS: 0,
                    penaltyW: 2000,
                    style: ['jsa-bubble','tool-notes-info-bubble'],
                    containerStyle: ['jsa-bubble-container','tool-notes-info-bubble-container'],
                });
                this.app.AddChild(this.infoBubble);

                this.infoBubble.notesList = new jsa.CustomFlatContainer({
                    style: ['notes-list']
                });
                this.infoBubble.AddChild(this.infoBubble.notesList);

                let self = this;
                this.infoBubble.clearButton = new jsa.Button({
                    content: 'Clear',
                    style: ['jsa-button','jsa-button-bottom'],
                    onClickCallback: function(e) {
                        self.ClearNotes();
                    }
                });
                this.infoBubble.AddChild(this.infoBubble.clearButton);

                this.RebuildNotesList();
            }
            this.infoBubble.PopupOnDomElement(this.GetDomElement());
        }
        return this;
    };

    NotesTool.prototype.Dissolve = function() {
        if(this.infoBubble) {
            this.infoBubble.Dissolve();
        }
        jsa.Tool.prototype.Dissolve.call(this);
    }

    NotesTool.prototype.AddNote = function(note) {
        if(this.infoBubble) {
            let content = '<small>('+note.id+') '+note.date.toString()+':</small>' +
                        '<p>'+ note.message+'</p>';

            let nodeDomElement = document.createElement('div');
            nodeDomElement.classList.add('note');
            switch(note.level) {
                case 'success':
                    nodeDomElement.classList.add('note-success');
                    break;
                case 'info':
                    nodeDomElement.classList.add('note-info');
                    break;
                case 'warning':
                    nodeDomElement.classList.add('note-warning');
                    break;
                case 'error':
                    nodeDomElement.classList.add('note-error');
                    break;
            }
            nodeDomElement.innerHTML = content;
            this.infoBubble.notesList.GetContainingDom().appendChild(nodeDomElement);
            this.shownNotes++;
        }
        return this;
    };

    NotesTool.prototype.RebuildNotesList = function(notes) {
        if(this.infoBubble) {
            this.infoBubble.notesList.SetContent(''); //clear the list
            if(this.notesManager) {
                let notes = this.notesManager.GetNotes();
                if(notes.length > 0) {
                    for(let i=0; i<notes.length; i++) {
                        let note = notes[i];
                        this.AddNote(note);
                    }
                    this.infoBubble.clearButton.Show();
                } else {
                    this.infoBubble.notesList.SetContent('No notes available'); //clear the list
                    this.infoBubble.clearButton.Hide();
                    this.shownNotes = 0;
                }
            }
        }
        return this;
    };

    NotesTool.prototype.ClearNotes = function() {
        if(this.notesManager) {
            this.notesManager.ClearNotes();
        }
        return this;
    };

    NotesTool.prototype.UpdateLabel = function() {
        let notesIndicationString = '';
        if(this.notesManager) {
            let nNotes = this.notesManager.GetNumberOfNotes();
            if(nNotes>0) {
                if(nNotes<1000) {
                    notesIndicationString = nNotes.toString();
                } else if (nNotes<1000000) {
                    notesIndicationString = (Math.floor(nNotes/1000).toString())+'K';
                } else if (nNotes<1000000000) {
                    notesIndicationString = (Math.floor(nNotes/1000000).toString())+'M';
                } else if (nNotes<1000000000000) {
                    notesIndicationString = (Math.floor(nNotes/1000000000).toString())+'G';
                } else {
                    notesIndicationString = '<1T';
                }
                if(this.newNotes) {
                    notesIndicationString += '!';
                }
            }
        }
        this.SetContent(notesIndicationString);
        return this;
    };

    return {
        NotesTool : NotesTool
    };
})());

