// XGEE mxGraph integration
// (C) 2019-2020 Institute of Aircraft Systems, Matthias Brunner

import Label from '../model/graph/Label.js'



// Disable bounding box calculation for mxText
// These calculations caused considerable performance issues and the function seems unnecessary for XGEE at the moment.
mxText.prototype.updateBoundingBox=()=>{}

//default styling
mxConstants.DEFAULT_FONTSIZE=18;
mxConstants.DEFAULT_FONTFAMILY="Helvetica Neue,Helvetica,Arial,Sans Serif";

// Determines whether a child is contrained
mxGraph.prototype.isConstrainChild = function(cell)
{
    let enforceConstraint=this.isConstrainChildren();
    
    if(cell.vertex && cell.value)
    {
        if(cell.value)
        {
            enforceConstraint=cell.value.isMovable();
        }
    }

	return  enforceConstraint &&!this.getModel().isEdge(this.getModel().getParent(cell));
};

//Add UUID to canvas elements
mxCellRenderer.prototype.getShapesForState = function(state)
{
    state.shape.node.id="uuid::"+state.cell.value.uuid;
	return [state.shape, state.text, state.control];
};

(function(){
    var vertexHandlerUnion = mxVertexHandler.prototype.union;
    mxVertexHandler.prototype.union = function(bounds, dx, dy, index, gridEnabled, scale, tr)
    {
        var result = vertexHandlerUnion.apply(this, arguments);

        if(this.state.cell.value.minSize.x>-1)
        {
            result.width = Math.max(result.width, this.state.cell.value.minSize.x);
        }
        if(this.state.cell.value.minSize.y>-1)
        {
            result.height = Math.max(result.height, this.state.cell.value.minSize.y);
        }
        if(this.state.cell.value.maxSize.x>-1)
        {
            result.width = Math.min(result.width, this.state.cell.value.maxSize.x);
        }
        if(this.state.cell.value.maxSize.y>-1)
        {
            result.height = Math.min(result.height, this.state.cell.value.maxSize.y);
        }

        return result;
    };
})();

mxCellRenderer.prototype.redrawLabel = function(state, forced)
{
	var graph = state.view.graph;
	var value = this.getLabelValue(state);
	var wrapping = graph.isWrapping(state.cell);
	var clipping = graph.isLabelClipped(state.cell);
	var isForceHtml = (state.view.graph.isHtmlLabel(state.cell) || (value != null && mxUtils.isNode(value)));
	var dialect = (isForceHtml) ? mxConstants.DIALECT_STRICTHTML : state.view.graph.dialect;
	var overflow = state.style[mxConstants.STYLE_OVERFLOW] || 'visible';

	if (state.text != null && (state.text.wrap != wrapping || state.text.clipped != clipping ||
		state.text.overflow != overflow || state.text.dialect != dialect))
	{
		state.text.destroy();
		state.text = null;
	}
	
	if (state.text == null && value != null && (mxUtils.isNode(value) || value.length > 0))
	{
		this.createLabel(state, value);
	}
	else if (state.text != null && (value == null || value.length == 0))
	{
		state.text.destroy();
		state.text = null;
	}

	if (state.text != null)
	{
		// Forced is true if the style has changed, so to get the updated
		// result in getLabelBounds we apply the new style to the shape
		if (forced)
		{
			// Checks if a full repaint is needed
			if (state.text.lastValue != null && this.isTextShapeInvalid(state, state.text))
			{
				// Forces a full repaint
				state.text.lastValue = null;
			}
			
			state.text.resetStyles();
			state.text.apply(state);
			
			// Special case where value is obtained via hook in graph
			state.text.valign = graph.getVerticalAlign(state);
		}
        
       

        state.text.getShapeRotation=function(){
            var cell=state.cell;
            if(cell.value)
            {
                if(cell.value instanceof Label)
                {                
                    if(cell.value.rotation!=null && !Number.isNaN(cell.value.rotation)) return cell.value.rotation
                }
                return 0
            }          
            return 0;            
        };

		var bounds = this.getLabelBounds(state);
		var nextScale = this.getTextScale(state);
		
		if (forced || state.text.value != value || state.text.isWrapping != wrapping ||
			state.text.overflow != overflow || state.text.isClipping != clipping ||
			state.text.scale != nextScale || state.text.dialect != dialect ||
			!state.text.bounds.equals(bounds))
		{
			// Forces an update of the text bounding box
			if (state.text.bounds.width != 0 && state.unscaledWidth != null &&
				Math.round((state.text.bounds.width /
				state.text.scale * nextScale) - bounds.width) != 0)
			{
				state.unscaledWidth = null;
			}
			
			state.text.dialect = dialect;
			state.text.value = value;
			state.text.bounds = bounds;
			state.text.scale = nextScale;
			state.text.wrap = wrapping;
			state.text.clipped = clipping;
			state.text.overflow = overflow;
            

			// Preserves visible state
			var vis = state.text.node.style.visibility;
			this.redrawLabelShape(state.text);
			state.text.node.style.visibility = vis;
		}
	}
};

mxGraphView.prototype.updateVertexLabelOffset = function(state)
{
	var h = mxUtils.getValue(state.style, mxConstants.STYLE_LABEL_POSITION, mxConstants.ALIGN_CENTER);

	if (h == mxConstants.ALIGN_LEFT)
	{
		var lw = mxUtils.getValue(state.style, mxConstants.STYLE_LABEL_WIDTH, null);
		
		if (lw != null)
		{
			lw *= this.scale;
		}
		else
		{
			lw = state.width;
		}
		
		state.absoluteOffset.x -= lw;
	}
	else if (h == mxConstants.ALIGN_RIGHT)
	{
		state.absoluteOffset.x += state.width;
	}
	else if (h == mxConstants.ALIGN_CENTER)
	{
		var lw = mxUtils.getValue(state.style, mxConstants.STYLE_LABEL_WIDTH, null);
		
		if (lw != null)
		{
			// Aligns text block with given width inside the vertex width
			var align = mxUtils.getValue(state.style, mxConstants.STYLE_ALIGN, mxConstants.ALIGN_CENTER);
			var dx = 0;
			
			if (align == mxConstants.ALIGN_CENTER)
			{
				dx = 0.5;
			}
			else if (align == mxConstants.ALIGN_RIGHT)
			{
				dx = 1;
			}
			
			if (dx != 0)
			{
				state.absoluteOffset.x -= (lw * this.scale - state.width) * dx;
			}
		}
	}
	
	var v = mxUtils.getValue(state.style, mxConstants.STYLE_VERTICAL_LABEL_POSITION, mxConstants.ALIGN_MIDDLE);
	
	if (v == mxConstants.ALIGN_TOP)
	{
		state.absoluteOffset.y -= state.height;
	}
	else if (v == mxConstants.ALIGN_BOTTOM)
	{
		state.absoluteOffset.y += state.height;
    }
    
    // Add the user-defined label offset
    var cell=state.cell;
    if(cell.value)
    {
        if(cell.value.__displayableObject)
        {
            state.absoluteOffset.x += this.scale*cell.value.__displayableObject.get("labelOffsetX");
            state.absoluteOffset.y += this.scale*cell.value.__displayableObject.get("labelOffsetY");
        }
    }
};

export {}