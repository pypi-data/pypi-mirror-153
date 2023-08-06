var ports = new Array();
var ports_GATE_OR=[];
var ports_GATE_AND=[];
var ports_EVENT=[];


function configEditorConnectionBehavior()
{
}
function enablePorts(graph)
{
	//Connection Points
		mxConstraintHandler.prototype.pointImage = new mxImage('ui/dot.gif', 10, 10);
		graph.setPortsEnabled(false);

	// NOTE: Constraint is used later for orthogonal edge routing (currently ignored)
		ports_GATE_OR['n'] = {x: 0.5, y: 0.05, perimeter: false, constraint: 'north'};
		ports_GATE_OR['s'] = {x: 0.5, y: 0.908, perimeter: false, constraint: 'south'};
		ports_GATE_AND['n'] = {x: 0.5, y: 0.05, perimeter: false, constraint: 'north'};
		ports_GATE_AND['s'] = {x: 0.5, y: 1, perimeter: false, constraint: 'south'};
		ports_EVENT['n'] = {x: 0.5, y: 0.05, perimeter: false, constraint: 'north'};
		ports_EVENT['s'] = {x: 0.5, y: 1, perimeter: false, constraint: 'south'};

		ports=ports_GATE_OR;
	// Extends shapes classes to return their ports
		mxShape.prototype.getPorts = function()
		{
		return ports;
		};
			
			
	// Disables floating connections (only connections via ports allowed)
		graph.connectionHandler.isConnectableCell = function(cell)
		{
		return false;
		};

		mxEdgeHandler.prototype.isConnectableCell = function(cell)
		{
		return graph.connectionHandler.isConnectableCell(cell);
		};

	// Disables existing port functionality
		graph.view.getTerminalPort = function(state, terminal, source)
		{
		return terminal;
		};
		

	// Returns all possible ports for a given terminal
		graph.getAllConnectionConstraints = function(terminal, source)
		{
		if (terminal != null && terminal.shape != null &&
			terminal.shape.stencil != null)
		{
			// for stencils with existing constraints...
			if (terminal.shape.stencil != null)
			{
				return terminal.shape.stencil.constraints;
			}
		}
		else if (terminal != null && this.model.isVertex(terminal.cell))
		{
			if (terminal.shape != null)
			{
				var ports = terminal.shape.getPorts();
				var cstrs = new Array();
				
				for (var id in ports)
				{
					var port = ports[id];
					
					var cstr = new mxConnectionConstraint(new mxPoint(port.x, port.y), port.perimeter);
					cstr.id = id;
					cstrs.push(cstr);
				}
				
				return cstrs;
			}
		}

		return null;
		};

	// Sets the port for the given connection
		graph.setConnectionConstraint = function(edge, terminal, source, constraint)
		{
		if (constraint != null)
		{
			var key = (source) ? mxConstants.STYLE_SOURCE_PORT : mxConstants.STYLE_TARGET_PORT;
			
			if (constraint == null || constraint.id == null)
			{
				this.setCellStyles(key, null, [edge]);
			}
			else if (constraint.id != null)
			{
				this.setCellStyles(key, constraint.id, [edge]);
			}
		}
		};

	// Returns the port for the given connection
		graph.getConnectionConstraint = function(edge, terminal, source)
		{
		var key = (source) ? mxConstants.STYLE_SOURCE_PORT : mxConstants.STYLE_TARGET_PORT;
		var id = edge.style[key];

		if (id != null)
		{
			var c =  new mxConnectionConstraint(null, null);
			c.id = id;
			
			return c;
		}

		return null;
		};

	// Returns the actual point for a port by redirecting the constraint to the port
		graphGetConnectionPoint = graph.getConnectionPoint;
		graph.getConnectionPoint = function(vertex, constraint)
		{
		if (constraint.id != null && vertex != null && vertex.shape != null)
		{
			var port = vertex.shape.getPorts()[constraint.id];
			
			if (port != null)
			{
				constraint = new mxConnectionConstraint(new mxPoint(port.x, port.y), port.perimeter);
			}
		}

		return graphGetConnectionPoint.apply(this, arguments);
		};
		
}