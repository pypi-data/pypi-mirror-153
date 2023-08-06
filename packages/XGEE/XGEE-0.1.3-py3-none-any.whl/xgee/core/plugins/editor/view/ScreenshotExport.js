/**
 * Screenshot Export module
 * @author Matthias Brunner
 * @copyright 2019-2021 University of Stuttgart, Institute of Aircraft Systems, Matthias Brunner
*/


/** Saves a SVG DOM element to a svg file
 * @private
*/

function showExportModal(svg){
    let modal = new jsa.Modal({
    name:'Save screenshot',
    content: '<form>' +
        '    <div class="row">' +
        '   <div class="jsa-row">' +
        '    <label for="XGEEscreenshotName" class="jsa-col-20">Name</label>' +
        '    <div class="jsa-col-80">' +
        '      <input type="text" class="jsa-text-ctrl-input" id="XGEEscreenshotName" placeholder="Name" value="GraphSreenshot">' +
        '    </div>' +
        '  </div>' +
        '      <legend class="col-form-label col-sm-2 pt-0"><b>Scope</b></legend>' +
        '      <div class="col-sm-10">' +
        '        <div class="jsa-radio-ctrl">' +
        '          <input class="jsa-radio-ctrl-input" type="radio" name="XGEEscreenshotScope" id="XGEEscreenshotScopeCurrentView" value="currentView" checked>' +
        '          <label class="jsa-radio-ctrl-label" for="XGEEscreenshotScopeCurrentView">' +
        '            Current view' +
        '          </label>' +
        '        </div>' +
        '        <div class="jsa-radio-ctrl">' +
        '          <input class="jsa-radio-ctrl-input" type="radio" name="XGEEscreenshotScope" id="XGEEscreenshotScopeCompleteGraph" value="completeGraph">' +
        '          <label class="jsa-radio-ctrl-label" for="XGEEscreenshotScopeCompleteGraph">' +
        '            Complete graph' +
        '          </label>' +
        '        </div>' +
        '      </div>' +
        '    </div><br>' +
        '  <div class="form-group row">' +
        '    <div class="col-sm-2"><b>Options</b></div>' +
        '    <div class="col-sm-10">' +
        '      <div class="jsa-checkbox-ctrl">' +
        '        <input class="jsa-checkbox-ctrl-input" type="checkbox" id="XGEEscreenshotHTMLConversion" >'+
        '        <label class="jsa-checkbox-ctrl-label" for="XGEEscreenshotHTMLConversion">' +
        '          Convert HTML to plain text' +
        '        </label>' +
        '      </div>' +      
        '    </div>' +
        '  </div>' +
        '</form>',

    buttons: {
        ok: {
            name: 'Save screenshot',
            startEnabled: true,
            onClickCallback: function(event) {
                let screenshotName=$("#XGEEscreenshotName").val();
                let screenshotScope=$("input:radio[name ='XGEEscreenshotScope']:checked").val();
                let screenshotConvertHTML=$("#XGEEscreenshotHTMLConversion").is(':checked');
                
                if(!screenshotName.length)
                {
                    screenshotName='UnnamedScreenshot'
                }
                let exportSVG=svg
                if(screenshotConvertHTML)
                {
                    exportSVG=convertForeignObjects(svg)   
                }
                
                if(screenshotScope=='completeGraph')
                {
                    $(exportSVG).find('g')[0].removeAttribute('transform')  
                }

                modal.Dissolve()
                saveSVG(exportSVG,screenshotName)
               
            }
        },
        cancel: {
            name: 'Cancel',
            startEnabled: true,
            onClickCallback: function(event) {
                modal.Dissolve()
            }
        }
     }
    });
    $app.AddChild(modal);
}
function saveSVG(svg,name)
{
    let data = (new XMLSerializer()).serializeToString(svg);
    let blob = new Blob([data], {type: 'image/svg+xml;charset=utf-8'});
    let svgURL=URL.createObjectURL(blob)
  
    //Appending hidden link
    var downloadLink = document.createElement('a');
    downloadLink.setAttribute('href', svgURL);
    downloadLink.setAttribute('download', name+'.svg');
    downloadLink.setAttribute('target', '_blank');
    downloadLink.style.display = 'none';
    document.body.appendChild(downloadLink);

    downloadLink.click();
    document.body.removeChild(downloadLink);

    URL.revokeObjectURL(svgURL)    
}

/** Converts foreign objects in a SVG DOM element to text
 * @private
*/
function convertForeignObjects(originalSVG)
{
    let svg=originalSVG.cloneNode(true)      
    let foreignObjects=$(svg).find('foreignObject').toArray()
    foreignObjects.forEach((foreignObject)=>{
        var text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.innerHTML=$(foreignObject).text()
        let paddingTop=$($(foreignObject).find('div')[0]).css('padding-top').replace('px','')
        let marginLeft=$($(foreignObject).find('div')[0]).css('margin-left').replace('px','')
        text.setAttribute('x',marginLeft)
        text.setAttribute('y',paddingTop)

        //Text anchoring from CSS
        let textAnchor='middle'
        let textAlign=$(foreignObject).children('div').children('div').first().css('text-align')
        if(textAlign=='left')
        {
            textAnchor='start'
        } else if( textAlign == 'right')
        {
            textAnchor='end'
        } else if( textAlign == 'center')
        {
            textAnchor='middle'
        }

        text.setAttribute('text-anchor',textAnchor)
       $(foreignObject).replaceWith(text)
    })
    return svg
}


/** Gets the currently shown graph's SVG
 * @private
*/
function getGraphSVG()
{
    return $($app.viewManager.GetActiveView().editorCanvas).find('svg')[0]
}

/** Runs the SVG export
 * @private
*/
function exportSVG()
{
    let graphSVG=getGraphSVG()
    let svg=graphSVG.cloneNode(true)    
    showExportModal(svg)
}

var ScreenshotExport={
    'getGraphSVG': getGraphSVG,
    'exportSVG': exportSVG,
    'convertForeignObjects': convertForeignObjects,
    'showExportModal': showExportModal
}

export default ScreenshotExport