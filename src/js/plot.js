function D3Backend (plot, container) {
  this.plot = plot

  this.svg = d3.select(container)
    .append('svg')
    .attr({
      width: plot.width(),
      height: plot.height(),
      version: '1.1',
      xmlns: 'http://www.w3.org/2000/svg'
    })

  this.svg.on('mouseover', () => this.updateCrosshair({ x: d3.event.offsetX, y: d3.event.offsetY }))

  this.zoom = d3.behavior.zoom()
    .size([this.plot.width(), this.plot.height()])
    .x(this.plot.scales.x)
    .y(this.plot.scales.y)
  this.zoom.on('zoom', this._handleZoom.bind(this))
  this.svg.call(this.zoom)
  this.graphs = []
}

D3Backend.prototype._handleZoom = function () {
  this.updateAxes()
  this.updateGrid()
  for (let i = 0; i < this.graphs.length; i++) {
    this.graphs[i].update()
  }
  if (d3.event !== null) {
    this.plot.retrieveData({ scale: d3.event.scale })
  }
}

D3Backend.prototype.showAxes = function () {
  this.svg.select('.axes').remove()
  this.axes = this.svg.append('g').attr('class', 'axes')
  this.xAxis = d3.svg.axis().scale(this.plot.scales.x).orient('bottom').ticks(10).tickSize(2)
  this.yAxis = d3.svg.axis().scale(this.plot.scales.y).orient('right').ticks(10).tickSize(2)
  this.axes.append('g').attr('class', 'x-axis')
  this.axes.append('g').attr('class', 'y-axis')
  this.updateAxes()
}

D3Backend.prototype.hideAxes = function () {
  this.svg.select('.axes').remove()
}

D3Backend.prototype.updateAxes = function () {
  this.axes.select('.x-axis').call(this.xAxis)
  this.axes.select('.y-axis').call(this.yAxis)
  let yPos = this.plot.scales.y(0) - 0.5
  this.xAxis.orient('bottom')
  if (yPos > this.plot.height()) {
    yPos = this.plot.height()
    this.xAxis.orient('top')
  } else if (yPos < 0) {
    yPos = 0
  }
  let xPos = this.plot.scales.x(0) - 0.5
  this.yAxis.orient('right')
  if (xPos > this.plot.width()) {
    xPos = this.plot.width()
    this.yAxis.orient('left')
  } else if (xPos < 0) {
    xPos = 0
  }
  this.svg.select('.x-axis').attr('transform', 'translate(0,' + yPos + ')')
  this.svg.select('.y-axis').attr('transform', 'translate(' + xPos + ', 0)')
}

D3Backend.prototype.showGrid = function () {
  this.svg.select('.grid').remove()
  this.grid = this.svg.append('g').attr('class', 'grid')
  this.xGrid = this.grid.append('g').attr('class', 'x-grid')
  this.yGrid = this.grid.append('g').attr('class', 'y-grid')
  this.updateGrid()
}

D3Backend.prototype.hideGrid = function () {
  this.svg.select('.grid').remove()
}

D3Backend.prototype.updateGrid = function () {
  const x = this.xGrid.selectAll('line').data(this.plot.scales.x.ticks(10))
  x.enter().append('line')
  x.exit().remove()
  x.attr({
    x1: this.plot.scales.x,
    y1: this.plot.scales.y(this.plot.scales.y.domain()[1]),
    x2: this.plot.scales.x,
    y2: this.plot.scales.y(this.plot.scales.y.domain()[0]),
    fill: 'none',
    stroke: d3.rgb(125, 125, 125)
  }).attr('stroke-dasharray', '1, 3')

  const y = this.yGrid.selectAll('line').data(this.plot.scales.y.ticks(10))
  y.enter().append('line')
  y.exit().remove()
  y.attr({
    x1: this.plot.scales.x(this.plot.scales.x.domain()[0]),
    y1: this.plot.scales.y,
    x2: this.plot.scales.x(this.plot.scales.x.domain()[1]),
    y2: this.plot.scales.y,
    fill: 'none',
    stroke: d3.rgb(125, 125, 125)
  }).attr('stroke-dasharray', '1, 3')
}

D3Backend.prototype.showCrosshair = function () {
  this.crosshair = this.svg.append('g').attr('class', 'crosshair')
  this.crosshair.append('line').attr({
    class: 'x',
    x1: 0,
    y1: 0,
    fill: 'none',
    stroke: d3.rgb(25, 25, 25)
  })
  this.crosshair.append('line').attr({
    class: 'y',
    x1: 0,
    y1: 0,
    fill: 'none',
    stroke: d3.rgb(25, 25, 25)
  })
  this.updateCrosshair({ x: 0, y: 0 })
}

D3Backend.prototype.hideCrosshair = function () {
  this.svg.select('.crosshair').remove()
}

D3Backend.prototype.updateCrosshair = function (offset) {
  this.crosshair.select('.x').attr({
    y1: offset.y,
    x2: this.plot.scales.x(this.plot.scales.x.domain()[1]),
    y2: offset.y
  })
  this.crosshair.select('.y').attr({
    x1: offset.x,
    x2: offset.x,
    y2: this.plot.scales.y(this.plot.scales.y.domain()[0])
  })
}

D3Backend.prototype.makeGraph = function (graph, color) {
  const points = this.svg.append('g').attr('class', 'points')
  const path = this.svg.append('g').attr('class', 'path').append('svg:path')
  const line = d3.svg.line().x(this.plot.scales.x)

  const updatePoints = function (graph) {
    const circles = points.selectAll('circle')
      .data(graph.points.x)
    circles.exit().remove('circle')
    circles.enter().append('circle')
    points.selectAll('circle')
      .attr({
        cx: this.plot.scales.x,
        cy: function (value, index) {
          return this.plot.scales.y(graph.points.y[index])
        }.bind(this),
        r: 2,
        fill: color
      })
  }.bind(this)
  const updateLine = function (graph) {
    line.x(this.plot.scales.x)
      .y(function (value, index) {
        return this.plot.scales.y(graph.points.y[index])
      }.bind(this))
    path.attr({
      d: line(graph.points.x),
      fill: 'none',
      stroke: color,
      opacity: 0.8
    }).attr('stroke-width', 1.5)
  }.bind(this)

  let visible = true
  const g = {
    update: function (_graph) {
      if (typeof _graph !== 'undefined') {
        graph = _graph
      }
      if (this.plot.option('points')) {
        updatePoints(graph)
        points.attr('display', 'block')
      } else {
        points.attr('display', 'none')
      }

      if (this.plot.option('path')) {
        updateLine(graph)
        path.attr('display', 'block')
      } else {
        path.attr('display', 'none')
      }
    }.bind(this),

    toggle: function () {
      if (visible) {
        path.attr('display', 'none')
        points.attr('display', 'none')
      } else {
        this.update()
      }
      visible = !visible
    },

    highlight: function (highlight) {
      if (highlight) {
        path.attr('stroke-width', 3)
        points.selectAll('circle').attr('r', 3)
      } else {
        path.attr('stroke-width', 1.5)
        points.selectAll('circle').attr('r', 2)
      }
    }
  }
  this.graphs.push(g)
  return g
}

D3Backend.prototype.resize = function (options) {
  this.svg.attr({
    width: this.plot.width(),
    height: this.plot.height()
  })
  if (typeof options !== 'undefined' && options.updateZoom) {
    this.zoom
      .size([this.plot.width(), this.plot.height()])
      .x(this.plot.scales.x)
      .y(this.plot.scales.y)
  }
}

D3Backend.prototype.reset = function () {
  d3.transition().duration(300).tween('zoom', function () {
    const x = this.plot.scales.x
    const y = this.plot.scales.y
    const ix = d3.interpolate(x.domain(), [-10, 10])
    const iy = d3.interpolate(y.domain(), this.plot.calculateYRange())
    return function (t) {
      this.zoom.x(x.domain(ix(t))).y(y.domain(iy(t)))
      this._handleZoom()
    }.bind(this)
  }.bind(this))
}

D3Backend.prototype.asDataURI = function () {
  // http://stackoverflow.com/questions/2483919
  this.hideCrosshair()
  const serializer = new XMLSerializer()
  const svgData = window.btoa(serializer.serializeToString(this.svg[0][0]))
  this.showCrosshair()
  return 'data:image/svg+xml;base64,\n' + svgData
}

function Plot2D (container, graphs, reevaluate) {
  this.container = container
  this._graphs = graphs
  this.reevaluate = reevaluate
  this.graphs = []
  this.options = ['grid', 'axes', 'path']

  this._scale = 1
  this._requestPending = false

  this._generateScales()
  this._backend = new D3Backend(this, container)
  this._calculateExtent()
}

Plot2D.prototype._generateScales = function () {
  if (typeof this.scales === 'undefined') {
    this.scales = {
      x: d3.scale.linear(),
      y: d3.scale.linear()
    }
  }
  this.scales.x.domain([-10, 10]).range([0, this.width()])
  this.scales.y.domain(this.calculateYRange()).range([this.height(), 0])
}

Plot2D.prototype._calculateExtent = function () {
  this._extent = {
    min: d3.min(this._graphs.map(function (g) { return d3.min(g.points.x) })),
    max: d3.max(this._graphs.map(function (g) { return d3.max(g.points.x) }))
  }
}

Plot2D.prototype.calculateYRange = function () {
  if (typeof this._originalExtent !== 'undefined') {
    return this._originalExtent
  }

  const ypos = []
  const yneg = []
  let ytop = 0
  let ybottom = 0
  this._graphs.forEach(function (graph) {
    graph.points.y.forEach(function (y) {
      if (y < ybottom) {
        ybottom = y
      } else if (y > ytop) {
        ytop = y
      }

      if (y <= 0) {
        yneg.push(y)
      } else if (y > 0) {
        ypos.push(y)
      }
    })
  })

  const yposmean = Math.abs(d3.mean(ypos))
  const ynegmean = Math.abs(d3.mean(yneg))

  // Prevent asymptotes from dominating the graph
  if (Math.abs(ytop) >= 10 * yposmean) {
    ytop = yposmean
  }
  if (Math.abs(ybottom) >= 10 * ynegmean) {
    ybottom = -ynegmean
  }
  this._originalExtent = [ybottom, ytop]
  return this._originalExtent
}

Plot2D.prototype.width = function () {
  return Math.round(this.container.offsetWidth)
}

Plot2D.prototype.height = function () {
  return Math.round(this.container.offsetHeight)
}

Plot2D.prototype.show = function () {
  this._backend.showAxes(this.scales)
  this._backend.showGrid(this.scales)

  const colors = d3.scale.category10()
  for (let i = 0; i < this._graphs.length; i++) {
    const graph = this._backend.makeGraph(this._graphs[i], colors(i))
    graph.update()
    this.graphs.push(graph)
  }

  this._backend.showCrosshair()
}

Plot2D.prototype.update = function () {
  if (this.option('axes')) {
    this._backend.showAxes(this.scales)
  } else {
    this._backend.hideAxes()
  }

  if (this.option('grid')) {
    this._backend.showGrid(this.scales)
  } else {
    this._backend.hideGrid()
  }

  for (let i = 0; i < this.graphs.length; i++) {
    const graph = this.graphs[i]
    graph.update()
  }
}

Plot2D.prototype.retrieveData = function (view) {
  if (view.scale !== this._scale) {
    this._scale = view.scale
    this.fetch(this.scales.x.domain()[0], this.scales.x.domain()[1], 'replace')
  } else {
    const half = (this._extent.max - this._extent.min) / 2
    if (this.scales.x.domain()[0] < this._extent.min) {
      this.fetch(Math.round(this.scales.x.domain()[0] - half), this._extent.min, 'prepend')
    }
    if (this.scales.x.domain()[1] > this._extent.max) {
      this.fetch(this._extent.max, Math.round(this.scales.x.domain()[1] + half), 'append')
    }
  }
}

// mode: replace, prepend, or append
Plot2D.prototype.fetch = async function (xMin, xMax, mode) {
  if (this._requestPending) {
    return
  }
  this._requestPending = true
  const parameters = { xmin: xMin, xmax: xMax }
  const data = await this.reevaluate(parameters)
  if (mode === 'replace') {
    this._graphs = data
  } else if (mode === 'prepend') {
    for (let i = 0; i < this.graphs.length; i++) {
      const graph = this._graphs[i]
      data[i].points.x.pop()
      data[i].points.y.pop()
      graph.points.x = data[i].points.x.concat(graph.points.x)
      graph.points.y = data[i].points.y.concat(graph.points.y)
    }
  } else if (mode === 'append') {
    for (let i = 0; i < this.graphs.length; i++) {
      const graph = this._graphs[i]
      data[i].points.x.shift()
      data[i].points.y.shift()
      graph.points.x = graph.points.x.concat(data[i].points.x)
      graph.points.y = graph.points.y.concat(data[i].points.y)
    }
  }

  for (let i = 0; i < this.graphs.length; i++) {
    this.graphs[i].update(this._graphs[i])
  }
  this._calculateExtent()
  this._requestPending = false
}

Plot2D.prototype.toggle = function (index) {
  this.graphs[index].toggle()
}

Plot2D.prototype.highlight = function (index, highlight) {
  this.graphs[index].highlight(highlight)
}

Plot2D.prototype.resize = function (options) {
  this.scales.x.range([0, this.width()])
  this.scales.y.range([this.height(), 0])
  this._backend.resize(options)
  this.update()
}

Plot2D.prototype.reset = function () {
  this._backend.reset()
  setTimeout(function () {
    this.retrieveData({ scale: 1 })
  }.bind(this), 300)
}

Plot2D.prototype.setOption = function (options) {
  this.options = options
}

Plot2D.prototype.option = function (opt, value) {
  if (typeof value === 'undefined') {
    return this.options.indexOf(opt) >= 0
  }
}

Plot2D.prototype.asDataURI = function () {
  return this._backend.asDataURI()
}

export { Plot2D }
