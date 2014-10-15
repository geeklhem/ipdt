"""export.py: export facilities"""
from __future__ import division
import re 
import time 
import math

CSS = """
body {
  background-color:#073642;
}

a {
  color:#268BD2;
  text-decoration:none;
  font-weight:bold;
}

a:visited {color:#6C71C4}
a:hover {color:#2AA198}

#Container {
  margin:auto;
  padding:0;
  min-width:34rem;
  max-width:42rem;
}

header {
  margin:1rem auto;
  padding:0.9rem;
  background-color:#002B36;
  font-family:sans-serif;
  text-align:center;
  border-color:#1C1C1C;
  border-style:solid;
  border-width:1px;
  border-radius:5px;
  display:block;
}

header h1 {
  color:#CB4B16;
  margin:0;
}

th {
color:rgb(221,251, 255);
text-align:center;
  background-color: rgb(0,98, 110);
}
td
{
  background-color: rgb(0,179, 200);
color:black;
text-align:center;
}

.blue
{
  background-color: rgb(0,179, 200);
}

.green
{
  background-color: rgb(133, 153, 0);
}

.yellow
{
  background-color: #b58900;
}

.red
{
  background-color:  rgb(203, 75, 22);
}

.max
{
  font-weight: bold;
}

strong[title]:hover:after
{
  background-color:#1C1C1C;
  color: rgb(0,179, 200);
}

#Content {
  padding:0 1.5rem;
  font-size:medium;
  font-family:sans-serif;
  font-size:medium;
  text-align:justify;
  color:#839496;
  background-color:#002B36;
  border-color:#1C1C1C;
  border-style:solid;
  border-width:1px 1px;
  border-radius:5px;
}

#Content img {
  width:100%;
  max-width:480px;
  height:auto;
}

#Content h1 {
  color:#B58900;
}

#Content h2 {
  color:#859900;
}

footer {
  padding-bottom:1rem;
  text-align:right;
  font-size:small;
  font-style:oblique;
}

pre .bash {
  font-family:monospace;
  text-align:left;
}

#chart svg {
  height: 400px;
  color: white;
}

#ts th, #ts td {
  color: black;
  text-align:center;
  background-color: white;
}



"""

TEMPLATE = """
<!DOCTYPE html>
<html>

<head>
<meta charset="utf-8" />

<title> 
{title}
</title>
<link rel="stylesheet" href="http://www.eleves.ens.fr/home/doulcier/projects/math/nv.d3.css"></link>
<style>
{css}
</style>
</head>

<body>
<div id="Container">
<header><h1> {title}</h1> </header>
<div id="Content">
{body}
<footer>{footer}</footer>
</div>
</div>

</body>
</html>
"""

SCRIPT ="""

<script src="http://www.eleves.ens.fr/home/doulcier/projects/math/d3.v3.js"></script>
<script src="http://www.eleves.ens.fr/home/doulcier/projects/math/nv.d3.min.js"></script>

<script>
var data = {data}
nv.addGraph(function() {{
  var chart = nv.models.stackedAreaChart()
                .x(function(d) {{ return d[0] }})
                .y(function(d) {{ return d[1] }})
                .clipEdge(true)
                .useInteractiveGuideline(true)
                ;

  chart.xAxis
      .showMaxMin(false)
;

  chart.yAxis
      .tickFormat(d3.format(',.2f'));

  d3.select('#chart svg')
    .datum(data)
      .transition().duration(500).call(chart);

  nv.utils.windowResize(chart.update);

  return chart;
}});



</script>
"""

FOOTER = '<a href="http://www.gt-mathsbio.biologie.ens.fr/">GT-MathsBio </a> -- Page generated on the {date} by <a href="https://github.com/geeklhem/ipdt"> ipdt</a>.'

class HTMLexporter(object):
    def __init__(self,path,ranking,payoff_matrix,param,info_strategies):
        self.path = path

        moves = sorted([(move, param[move]) for move in ["cc","dc","cd","dd"]],
                       key=lambda x:-x[1])  
        colors = ['class="green"','class="blue"','class="yellow"','class="red"']
        self.move_color = {}
        for n,move in enumerate(moves):
            self.move_color[move[0]] = colors[n] 

        
        self.sections = [
            ("info","Informations",self.general_info(param)),
            ("ranking","Ranking",self.ranking(ranking,info_strategies)),
            ("details","Detailed Results",self.details(zip(*ranking)[1], payoff_matrix,
                                                       info_strategies, param)),
        ]
        

    def general_info(self,param):
        s = "<p><em>This is the result of an iterated prisoner's dilemma tournament.</em></p>"
        s += "</p>The number of iteration per match is {} and the number of replicas is {}.</p>".format(param["T"],param["replicas"])
        s += "<p> The payoff matrix is: </p>"
        
        s+= """
        <table border="0" cellpadding="3" cellspacing="3">
	<tr>
		<th></th>
		<th>Cooperate</th>
		<th>Defect</th>
	</tr>
	<tr>
		<th>Cooperate</th>
		<td {1[cc]}>{0[cc]}</td>
		<td {1[cd]}>{0[cd]}</td>
	</tr>
	<tr>
		<th>Defect</th>
		<td {1[dc]}>{0[dc]}</td>
		<td {1[dd]}>{0[dd]}</td>
	</tr>
        </table>
        """.format(param,self.move_color)


        return s


    def get_color(self,score,param):
        diff = sorted([(abs(score-param[m]*param["T"]*param["replicas"]),m)
                       for m in ["cc","dc","cd","dd"]],
                      key=lambda x:x[0])
        return(self.move_color[diff[0][1]])
    
    def details(self,order,po,info,param):
        s = '<table border="0" cellpadding="3" cellspacing="3">\n<tr><th></th>\n'

        max_po = max([max(po[k].values()) for k in order])
        min_po = min([min(po[k].values()) for k in order])
        
        norm = lambda x: int(100*(x - min_po) / (max_po-min_po)) 
        
        if len(order)>5:
            for n,k in enumerate(order) :
               info[k]["rank"] = n+1
            display = "rank"
        else:
            display = "name"
            
        for k in order :
            s += '<th title="{1}">{0}</th>'.format(info[k][display],info[k]["name"])
        s+= '</tr>\n'
        for k in order:
            s+= '<tr>\n'
            s += '<th title="{1}">{0}</th>'.format(info[k][display],info[k]["name"])
            for j in order:
                cl = self.get_color(po[k][j],param)
                if po[k][j] == max_po or po[k][j] == min_po:
                    cl = cl[:-1] + ' max"\''

                s+= '<td {0} title="{2} vs {3}: {4} pts">{1}</td>'.format(cl, norm(po[k][j]),
                                                                          info[k]["name"],
                                                                          info[j]["name"],
                                                                          po[k][j])
            s+= '</tr>\n'
        s += "</table>\n"
        s += ('<p>Total payoff over all replicas normalized in [0,100].<br/> '
              ' The cell color gives the nearest payoff in a mono-move strategy '
              ' (see payoff matrix for reference).</p>')
        
        s += ("<p><em>(Do a mouseover on each cell to get the strategies' names"
              " and non-normalized payoff.)</em></p>")
        return s

    def ranking(self,ranking,info):
        s = "<ol>\n"
        for score,code in ranking:
            s+= ("<li><strong title=\"{3}\">{1}</strong> "
                 "(<em>{2}</em>) - {0} pts </li>\n").format(score,
                                                            info[code]["name"],
                                                            info[code]["author"],
                                                            info[code]["description"])
        s += "</ol>\n"
        s += "<em>(Do a mouseover on the name of each strategy to get a short description.)</em>"
        return s

    def output(self):
        body = ""
        for code,title,text in self.sections:
            body += "\n\n<div id='{}'><h2>{}</h2>\n{}\n</div>".format(code,title,text)
        footer =  FOOTER.format(date=time.asctime())
        out = TEMPLATE.format(body=body, css=CSS, title="ipdt report",footer=footer)
        return out 

    def save(self):
        with open(self.path,'w') as f:
            f.write(self.output())



class HTMLexporterTS(HTMLexporter):
    def __init__(self,path,time_series,payoff_matrix,param,info_strategies):
        self.path = path

        moves = sorted([(move, param[move]) for move in ["cc","dc","cd","dd"]],
                       key=lambda x:-x[1])  
        colors = ['class="green"','class="blue"','class="yellow"','class="red"']
        self.move_color = {}
        for n,move in enumerate(moves):
            self.move_color[move[0]] = colors[n] 

        
        self.sections = [
            ("info","Informations",self.general_info(param)),
            ("ts","Time series",self.time_series_d3(time_series,info_strategies)),
            ("details","Detailed Results",self.details(time_series.keys(), payoff_matrix,
                                                       info_strategies, param)),
        ]

    def time_series_d3(self,time_series,info):
        data = "[\n"
        offset =  None
        for k,v in time_series.items():
            values = []
            if offset is None:
                offset =  [0]*len(v)
            for j,p in enumerate(v):
                values.append([j,p])
                offset[j] += p
            data += '{{ "key": "{}", "values":{}}},'.format(k,values)

        data += "]\n"
        s = SCRIPT.format(data=data)
        s += '<div id="chart"> <svg></svg> </div>'
        return s


if __name__ == "__main__":
    from ipdt.tournament import DEFAULT_PARAM as param
    a = HTMLexporter("test.html",
                     [(100,"defector"),(10,"naivecoop")],
                     {
                         "defector":{"naivecoop":100,"defector":0},
                         "naivecoop":{"naivecoop":200,"defector":-100}
                     },
                     param,
                     {
                         "defector":{"name":"Defector","author":"Axelrod"},
                         "naivecoop":{"name":"Naive cooperator","author":"Axelrod"}
                     })
    a.save()


