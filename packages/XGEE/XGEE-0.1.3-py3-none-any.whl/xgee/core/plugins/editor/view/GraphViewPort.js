/**
 * GraphViewPort module
 * @author Matthias Brunner
 * @copyright 2019-2021 University of Stuttgart, Institute of Aircraft Systems, Matthias Brunner
*/


/** Class managing the graph viewport */
class GraphViewPort{
    /**
     * Create a viewport for the DOM element.
     * @param {DOMelement} DOM - The DOM element of the viewport.
     * @param {number} width - The width of the viewport.
     * @param {number} height - The height of the viewport.
     * @param {number} [scale=1] - The scale of the viewport.
     * @param {number} [translateX=0] - The translate's x-coordinate of the viewport.
     * @param {number} [translateY=0] - The translate's y-coordinate of the viewport.
     */
    constructor(DOM,width,height,scale=1,translateX=0,translateY=0){
        this.zoomListeners=[]
        this.panListeners=[]
        this.updateListeners=[]
        var id = new Uint32Array(1);
        this.id=window.crypto.getRandomValues(id).toString();
        this.DOM=DOM
        this.scale=scale
        this.width=width
        this.height=height
        this.centerX=width/2
        this.centerY=height/2
        this.translate={x:translateX,y:translateY}
        this.updateTransformationMatrix()
    }

    /**
     * Gets the viewport's unique id.
     * @returns {string} The viewport's unique id.
    */
    getId(){
        return this.id
    }

    /**
     * Gets the viewport's DOM element.
     * @returns {DOMelement} The viewport's DOM element.
    */
    getDOM()
    {
        return this.DOM
    }

    /**
     * Gets the width of the viewport.
     * @returns {number} The viewport's width in pixels.
    */
    getWidth(){
        return this.width
    }

    /**
     * Gets the height of the viewport.
     * @returns {number} The viewport's height in pixels.
    */
    getHeight(){
        return this.height
    }
    
    /**
     * Sets the current scale. Causes a transformation matrix update.
     * @param {number} scale - The new scale of the viewport.
    */
    setScale(scale)
    {
        if(scale!=0 && scale != Infinity)
        {
            this.scale=scale
            this.updateTransformationMatrix()
        }
    }

    /**
     * Gets the current scale.
     * @returns {number} The current scale.
    */
    getScale(){
        return this.scale
    }

    /**
     * Sets the current translate. Causes a transformation matrix update.
     * @param {translate} translate - The current translate (e.g. {x:0,y:0})
    */
    setTranslate(translate)
    {
        if(translate.x!=null) this.translate.x=translate.x
        if(translate.y!=null) this.translate.y=translate.y    
        this.updateTransformationMatrix()
    }

    /**
     * Gets the current translate.
     * @returns {translate} The current translate (e.g. {x:0,y:0})
    */
    getTranslate(){
        return Object.assign({},this.translate)
    }


    /**
     * Gets the current display state of the viewport.
     * @returns {boolean} The current display state.
    */
    isActive(){
        return $(this.DOM).is(":visible")
    }   


    /**
     * Updates the transformation matrix based on the current center, translate and scale. Causes a viewport update.
    */
    updateTransformationMatrix(){
       let self=this
       this.transformationMatrix=[1, 0, 0, 1, this.translate.x, this.translate.y].map((e) => { return e*self.scale})

       this.transformationMatrix[4]+=(1-this.scale)*this.centerX
       this.transformationMatrix[5]+=(1-this.scale)*this.centerY

       this.invTransformationMatrix=this.invertTransformationMatrix()
       this.updateViewPort()
    }

    /**
     * Centers the viewport on a new center
     * @param {number} [centerX] - The x-coordinate of the new center.
     * @param {number} [centerY] - The y-coordinate of the new center.
    */
    recenter(centerX=null,centerY=null)
    {
        if(centerX!=null) this.centerX=centerX
        if(centerY!=null) this.centerY=centerY
        this.updateTransformationMatrix()
    }

    /**
     * Gets the current transformation matrix.
     * @returns {transformationMatrix} The current transformation matrix.
    */
    getTransformationMatrix(){
        return this.transformationMatrix
    }

    /**
     * Gets the inverse of the transformation matrix.
     * @returns {transformationMatrix} The inverse of the current transformation matrix.
    */
    getInverseTransformationMatrix(){
        return this.invTransformationMatrix
    }

    /**
     * Sets the transformation matrix.
     * @params {transformationMatrix} transformationMatrix - The current transformation matrix.
    */
    setTransformationMatrix(transformationMatrix)
    {
        if(Array.isArray(transformationMatrix) && transformationMatrix.length==5 && !transformationMatrix.some( val => { return Number.isNaN(val)}))
        {
            this.transformationMatrix=transformationMatrix
        }
    }

    /**
     * Inverts the current transformation matrix.
     * @see getInverseTransformationMatrix
     * @returns {invertedTransformationMatrix} The inverted transformation matrix.
    */
    invertTransformationMatrix(){
        let invTransformationMatrix=[0, 0, 0 ,0 ,0, 0]

        invTransformationMatrix[0]=this.transformationMatrix[3]/(this.transformationMatrix[0]*this.transformationMatrix[3]-this.transformationMatrix[1]*this.transformationMatrix[2])
        invTransformationMatrix[1]=this.transformationMatrix[1]/(this.transformationMatrix[1]*this.transformationMatrix[2]-this.transformationMatrix[0]*this.transformationMatrix[3])
        invTransformationMatrix[2]=this.transformationMatrix[2]/(this.transformationMatrix[1]*this.transformationMatrix[2]-this.transformationMatrix[0]*this.transformationMatrix[3])
        invTransformationMatrix[3]=this.transformationMatrix[0]/(this.transformationMatrix[0]*this.transformationMatrix[3]-this.transformationMatrix[1]*this.transformationMatrix[2])
        invTransformationMatrix[4]=(this.transformationMatrix[3]*this.transformationMatrix[4]-this.transformationMatrix[2]*this.transformationMatrix[5])/(this.transformationMatrix[1]*this.transformationMatrix[2]-this.transformationMatrix[0]*this.transformationMatrix[3])
        invTransformationMatrix[5]=(this.transformationMatrix[1]*this.transformationMatrix[4]-this.transformationMatrix[0]*this.transformationMatrix[5])/(this.transformationMatrix[0]*this.transformationMatrix[3]-this.transformationMatrix[1]*this.transformationMatrix[2])

        return invTransformationMatrix
    }

    
    /**
     * Fires the zoom event.
     * @async
     * @private
    */
    async _fireZoomEvent(){
        this.zoomListeners.forEach((cb) => { cb(this.scale) })
    }

    /**
     * Zooms the viewport by a given factor.
     * @param {number} factor - The factor to zoom by.
    */
    zoomBy(factor){
        if(factor!=0 && factor != Infinity)
        {
            this.scale=this.scale*factor
            this.updateTransformationMatrix()
            this._fireZoomEvent()
        }   
    }

    /**
     * Zooms the viewport to a given target coordinate and by a given factor.
     * @param {coordinate} target - The target coordiante to zoom to.
     * @param {number} [factor=1] - The factor to zoom by.
    */
    zoomTo(target,factor=1)
    {      

        let panScale=0.2/this.scale

        if(factor!=0 && factor != Infinity){ this.scale=this.scale*factor; }   

        let relX=(this.centerX-target.x)
        let relY=(this.centerY-target.y)  
        
        let panX=factor>=1 ? panScale*relX : -panScale*relX
        let panY=factor>=1 ? panScale*relY : -panScale*relY
        this.panBy({x:panX,y:panY})  

        this._fireZoomEvent()
        this._firePanEvent()

        this.updateTransformationMatrix()        
    }

    /**
     * Fires the pan event.
     * @async
     * @private
    */
    async _firePanEvent(){
        this.panListeners.forEach((cb) => { cb(Object.assign({},this.translate)) })
    }


    /**
     * Pans the viewport by the given vector.
     * @param {vector} vector - The 2D vector to pan the viewport by.
    */
    panBy(vector)
    {
        if(!Number.isNaN(vector.x) && !Number.isNaN(vector.y))
        {
            this.translate.x+=vector.x
            this.translate.y+=vector.y
            this.updateTransformationMatrix()
            this._firePanEvent()
        }
        else
        {
            throw 'pan operation unsuccessful: the vector must not contain NaN entries'
        }
    }

    
    /**
     * Pans the viewport to a new center.
     * @param {number} x - The x-coordinate of the new center.
     * @param {number} y - The y-coordinate of the new center.
    */
    panTo(x,y)
    {
        if(!Number.isNaN(x) && !Number.isNaN(y))
        {
            let newCenter={x:x,y:y}
            let currentCenter=this.toOriginalCoordinate({x:this.centerX,y:this.centerY})
            this.panBy({x:-(newCenter.x-currentCenter.x),y:-(newCenter.y-currentCenter.y)})
        }
        else
        {
            throw 'pan operation unsuccessful: x and y must not be NaN'
        }
    }

    /**
     * Pans the viewport by a given vector relative to a specified origin.
     * @param {coordinate} origin - The origin to which the pan operation should occur.
     * @param {vector} vector - The 2D vector to pan the viewport by.
    */
    panRelative(origin,vector)
    {
        this.translate.x=origin.x+vector.x/this.scale
        this.translate.y=origin.y+vector.y/this.scale
        this.updateTransformationMatrix()
        this._firePanEvent()
    }

    /**
     * Converts an original graph coordinate to the viewport coordinates.
     * @param {coordinate} coordinate - The viewport coordinate that should be converted (e.g. {x:0,y:0})
     * @returns {convertedCoordinate} The converted coordinate.
    */
    toViewportCoordinate(coordinate)
    {
        let xt=this.transformationMatrix[0]*coordinate.x+this.transformationMatrix[2]*coordinate.y+this.transformationMatrix[4]
        let yt=this.transformationMatrix[1]*coordinate.x+this.transformationMatrix[3]*coordinate.y+this.transformationMatrix[5]
        return {x:xt,y:yt}
    }

    /**
     * Converts a coordinate to the original graph coordinates.
     * @param {coordinate} coordinate - The original graph coordinate that should be converted (e.g. {x:0,y:0})
     * @returns {convertedCoordinate} The converted coordinate.
    */
    toOriginalCoordinate(coordinate)
    {
        let xt=this.invTransformationMatrix[0]*coordinate.x+this.invTransformationMatrix[2]*coordinate.y+this.invTransformationMatrix[4]
        let yt=this.invTransformationMatrix[1]*coordinate.x+this.invTransformationMatrix[3]*coordinate.y+this.invTransformationMatrix[5]
        return {x:xt,y:yt}
    }

    /**
     * Fires the update event.
     * @async
     * @private
    */
    async _fireUpdate(){
        this.updateListeners.forEach((cb) => { cb({scale: this.scale, translate: Object.assign({},this.translate)}) })
    }

    /**
     * Gets the viewport rectangle.
     * @returns {rectangle} The current viewport rectangle (e.g. {x:0,y:0,width:100,height:50})
    */
    getViewportRectangle(){
        let corner=this.toOriginalCoordinate({x:0,y:0}) //upper left corner 
        return {x:corner.x,y:corner.y,width:this.width/this.scale,height:this.height/this.scale}
    }

    /**
     * Sets the viewport rectangle.
     * @param {number} x - The x-coordinate of the upper left corner of the rectangle.
     * @param {number} y - The y-coordinate of the upper left corner of the rectangle.
     * @param {number} width - The width of the rectangle.
     * @param {number} height - The height of the rectangle.
    */
    setViewportRectangle(x,y,width,height)
    {
        let scaleX=this.width/width
        let scaleY=this.height/height

        if(scaleX==scaleY)
        {     
            this.panTo(x+width/2,y+height/2)         
            this.setScale(scaleX)                
        }
        else
        {
           let minScale=Math.min(scaleX,scaleY)
           this.panTo(x+width/2,y+height/2)    
           //this.setScale(minScale)
           console.warn('XGEE: the viewport rectangle has been adjusted to preserve the viewport aspect ratio')
        }
    }

    /**
     * Adjusts the viewport so that the supplied region is contained in the viewport.
     * @param {number} x - The x-coordinate of the upper left corner of the region.
     * @param {number} y - The y-coordinate of the upper left corner of the region.
     * @param {number} width - The width of the region.
     * @param {number} height - The height of the region.
    */
    adjustViewToRegion(x,y,width,height)
    {
        if(!this.containsRegion(x,y,width,height))
        {
            if(this.width/this.scale < width || this.height/this.scale < height)
            {
                this.panTo(x+width/2,y+height/2)
                let scaleX=this.width/width
                let scaleY=this.height/height
                let newScale=Math.min(scaleX,scaleY)     
                this.setScale(newScale)
            }
            else
            {
                let newCenter={x:x+width/2,y:y+height/2}
                this.panTo(newCenter.x,newCenter.y)
            }
        }
    }

    /**
     * Checks wether a rectangular region is contained in the viewport. 
     * @param {number} x - The x-coordinate of the upper left corner of the region.
     * @param {number} y - The y-coordinate of the upper left corner of the region.
     * @param {number} width - The width of the region.
     * @param {number} height - The height of the region.
     * @returns {boolean} The boolean indicating wether the region is contained.
    */
    containsRegion(x,y,width,height){
        let pt1={x:x,y:y}
        let pt2={x:x+width,y:y+height}
        return this.containsPoint(pt1) && this.containsPoint(pt2) 
    }

    /**
     * Checks wether a point is contained in the viewport. 
     * @param {point} Point - The point that should be checked (e.g. {x:0,y:0})
     * @returns {boolean} The boolean indicating wether the point is contained.
    */
    containsPoint(point){
        let viewPortRectangle=this.getViewportRectangle()
        let res=false
        if((point.x>=viewPortRectangle.x && point.x<=viewPortRectangle.x+viewPortRectangle.width) && (point.y>=viewPortRectangle.y && point.y<=viewPortRectangle.y+viewPortRectangle.height))
        {
            res=true
        }
        return res
    }

    /**
     * Updates the viewport. 
    */
    updateViewPort(){
       this.DOM.setAttribute('transform','matrix('+this.transformationMatrix.join(' ')+')')
       this._fireUpdate()
    }


     /**
     * Callback for pan event listeners.
     *
     * @callback panCallback
     * @param {obj} translate - The new translate of the viewport. (e.g. {x:0,y:0})
     */

    /**
     * Adds a event listener for pan events.
       @param {panCallback} callback - The callback function to be called when the event occurs.
    */
    onPan(callback){
        let self=this
        let unsubscribe=()=>{
            self.panListeners=self.panListeners.filter( (cb) => { return cb !== callback } )
        }
        
        if(!this.panListeners.includes(callback)){
            this.panListeners.push(callback)
        }

        return unsubscribe
    }

     /**
     * Callback for zoom event listeners.
     *
     * @callback zoomCallback
     * @param {number} scale - The new scale of the viewport.
     */

    /**
     * Adds a event listener for zoom events.
       @param {zoomCallback} callback - The callback function to be called when the event occurs.
    */
    onZoom(callback){
        let self=this
        let unsubscribe=()=>{
            self.zoomListeners=self.zoomListeners.filter( (cb) => { return cb !== callback } )
        }

        if(!this.zoomListeners.includes(callback)){
            this.zoomListeners.push(callback)
        }
        
        return unsubscribe
    }

    /**
     * Callback for update event listeners.
     *
     * @callback updateCallback
     * @param {obj} viewPortPropreties - An object containing the scale and translate.
     */

    /**
     * Adds a event listener for update events.
       @param {updateCallback} callback - The callback function to be called when the event occurs.
    */
    onUpdate(callback){
        let self=this
        let unsubscribe=()=>{
            self.updateListeners=self.updateListeners.filter( (cb) => { return cb !== callback } )
        }

        if(!this.updateListeners.includes(callback)){
            this.updateListeners.push(callback)
        }
        
        return unsubscribe
    }



    /**
     * Resets the viewport to the default scale (1.00) and the default translate (x=0, y=0).
    */
    reset(){
        this.scale=1
        this.translate={x:0,y:0}
        this.updateTransformationMatrix()
        this._firePanEvent()
        this._fireZoomEvent()
    }

}

/** Class managing the graph viewport outline*/
class GraphViewPortOutline{

    /**
     * Create a outline for a viewport.
     * @param {GraphViewPort} viewPort - The graph viewport for which the outline should be created.
     * @param {DOMelement} outlineDOM - The DOM element which should contain the graph view outline.
     */
    constructor(viewPort,outlineDOM)
    {
        var self=this
        this.viewPort=viewPort
        this.viewPortId=viewPort.getId()
        this.DOM=outlineDOM

        
        
        //Set outline parent DOM
        $(this.viewPort.getDOM()).find('g').get(1).setAttribute('id','outlineParent'+this.viewPortId)
        this.outlineParent=this.viewPort.getDOM()
    
        //Add outline
        this.DOM.innerHTML='<svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet" style="left: 0px; top: 0px; width:100%; height:100%; display: block; background-color:white; overflow:hidden; padding:10px; border-radius: var(--jsa-popup-bd-radius);"><g id="outlineViewportLayer'+this.viewPortId+'"><rect id="outlineViewportRect'+this.viewPortId+'" vector-effect="non-scaling-stroke" width="50%" height="50%" style="fill:#85c1e9;stroke-width:2;stroke:#3498db;fill-opacity:0.1;" /></g><g><use id="outlineReference'+this.viewPortId+'" href="#outlineParent'+this.viewPortId+'"></use></g></svg>';
        
        //Add listeners
        this.resizeObserver=new ResizeObserver((entries) => {            
            self.update()     
            self.updateActiveView()      
        })
        
        this.resizeObserver.observe(this.DOM)
        this.resizeObserver.observe($(this.outlineParent).parents('svg').get(0))
        this.update()
        this.updateActiveView()
        this.viewPort.onUpdate(()=>{
            self.updateActiveView()
        })
    }

    /**
     * Gets the width of the outline's DOM element.
     * @return {number} The DOM element's width in pixels.
    */
    getWidth(){
        return $(this.DOM).width()-20
    }


    /**
     * Gets the height of the outline's DOM element.
     * @return {number} The DOM element's height in pixels.
     */
    getHeight(){
        return $(this.DOM).height()-20
    }


    /**
     * Returns the visibility state of the original graph.
     * @return {boolean} True if the graph is visible, false otherwise.
    */
    isGraphVisible(){
        return $(this.outlineParent).is(":visible")
    }


    /**
     * Gets the width of the original graph.
     * @return {number} The original graph's width in pixels.
    */
    getGraphWidth(){
        let bbox=this.outlineParent.getBBox()
        return bbox.width
    }

    /**
     * Gets the height of the original graph.
     * @return {number} The original graph's height in pixels.
    */
    getGraphHeight(){
        let bbox=this.outlineParent.getBBox()
        return bbox.height
    }

    /**
     * Calculates the required scale of the outline on basis of the graph and outline size.
     * @return {number} The scale of the outline, where 1.00 means the outline uses the same scale as the graph.
    */
    calculateOutlineScale(){
        let result=1.0
        if(this.isGraphVisible() && Number.isFinite(this.getWidth()) && Number.isFinite(this.getHeight()) && this.getGraphWidth()!=0 && this.getGraphHeight()!=0)
        {
            let scaleX=this.getWidth()/this.getGraphWidth()
            let scaleY=this.getHeight()/this.getGraphHeight()
            result=Math.min(scaleX,scaleY)         
        }
        return result
    }

    /**
     * Calculates the translate of the viewport rectangle within the outline.
     * @return {number} The translate of the outline's viewport rectangle.
    */
    calculateOutlineTranslate(){
        let bbox=this.outlineParent.getBBox()
        return {x:-bbox.x,y:-bbox.y}
    }

    /**
     * Updates the outline upon changes of the viewport.
    */
    updateActiveView(){   
        if(this.viewPort.isActive())
        {     
            this.scale=this.calculateOutlineScale()    
            this.translate=this.calculateOutlineTranslate()           
            let viewPortRectangle=this.viewPort.getViewportRectangle()
            $("#outlineViewportRect"+this.viewPortId).get(0).setAttribute('width',viewPortRectangle.width)
            $("#outlineViewportRect"+this.viewPortId).get(0).setAttribute('height',viewPortRectangle.height)

            let viewportRectTranslate={x:-(viewPortRectangle.x),y:-(viewPortRectangle.y)}
        
            $('#outlineViewportRect'+this.viewPortId).get(0).setAttribute('transform','scale('+this.scale+') translate('+(this.translate.x-viewportRectTranslate.x)+','+(this.translate.y-viewportRectTranslate.y)+')')  
        }
    }

    /**
     * Updates the outline upon changes of model, e.g. enlarged graph due to added graph object.
    */
    update(){  
        if(this.viewPort.isActive())
        {   
            this.scale=this.calculateOutlineScale()    
            this.translate=this.calculateOutlineTranslate()         
            $('#outlineReference'+this.viewPortId).get(0).setAttribute('transform','scale('+this.scale+') translate('+this.translate.x+','+this.translate.y+')')   
            $('#outlineReference'+this.viewPortId).get(0).setAttribute('transform','scale('+this.scale+') translate('+this.translate.x+','+this.translate.y+')')  
        }
    }
}

export {GraphViewPort,GraphViewPortOutline}