poligonos=[] 
raios=[] 

colorIN=(255,0,255)
colorOUT=(0,255,255)
texto="Poligonos = botao esquerdo, Raios = botao direito"

mouseOnVert=False
chosenFigure=-1 
chosenVertex=-1 
polygonVertex=False
polygonDragged=-1
polygonDragged_Position=None

newPolygon=False
newRay=False
newVertex=False
OnPolygon=False
DragPolygon=False

def setup():
    size(640,360)
    smooth() 
    
def draw():
    fill(0,0,0)
    background(109,204,218)

    
    if newVertex or mouseOnVert or OnPolygon:
        cursor(HAND)
    else:
        cursor(CROSS);

    drawPolygon()
    drawRay()
    for raio in raios: draw_intersections(raio,True)

    #configurações do texto informativo
    textAlign(CENTER)
    text(texto,width/2,height-16)

def drawPolygon():
    #desenhando os polígonos
    for i,poligono in enumerate(poligonos):
        beginShape()
        fill(255,127)

        
        if i==(len(poligonos)-1) and newPolygon:
            stroke(0) 
            poligono=poligono[:]+[[mouseX,mouseY]]
        else:
            stroke(255) 

        for x,y in poligono:
            ellipse(x,y,5,5)
            vertex(x,y)
        endShape(CLOSE)
    fill(0,0,0)

def distPoint(x0,y0,x1,y1):
    dx,dy=x1-x0,y1-y0
    a=sqrt(width**2+height**2)
    if dy>0: x,y=x0+a*dx/abs(dy),y0+a
    elif dy<0: x,y=x0+a*dx/abs(dy),y0-a
    else:
        y=y0
        if dx>0: x=x0+a
        elif dx<0: x=x0-a
        else: x=x0
    return (x,y)

def intersection(p1,p2,q1,q2):
    det=(q2[0]-q1[0])*(p2[1]-p1[1])-(q2[1]-q1[1])*(p2[0]-p1[0])

    if det==0.0:
        return None

    else:
        s=((q2[0]-q1[0])*(q1[1]-p1[1])-(q2[1]-q1[1])*(q1[0]-p1[0]))/det
        x,y=p1[0]+(p2[0]-p1[0])*s,p1[1]+(p2[1]-p1[1])*s
        
        if width>=x>=0 and height>=y>=0 and (p2[0]>=x>=p1[0] or p1[0]>=x>=p2[0]) and (p2[1]>=y>=p1[1] or p1[1]>=y>=p2[1]) and (q2[0]>=x>=q1[0] or q1[0]>=x>=q2[0]) and (q2[1]>=y>=q1[1] or q1[1]>=y>=q2[1]):
                return [x,y]
        else:
            return None

def pointDistance(p1,p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def draw_intersections(raio,desenhar):
    if len(raio)==1:
        raio=raio[:]+[[mouseX,mouseY]]
    p1,p2=raio
    p2=distPoint(p1[0],p1[1],p2[0],p2[1])
    intersecoes=[]
    for ind,poligono in enumerate(poligonos):
        for i in range(len(poligono)):
            j=(i+1)%len(poligono)
            p3,p4=poligono[i],poligono[j]
            intersecao=intersection(p1,p2,p3,p4)
            if intersecao:
                intersecoes.append(intersecao)
        
        lista=[]
        for p in intersecoes:
            lista.append([pointDistance(p1,p),p])
        lista.sort()
        lista=[i[1] for i in lista]

        dentro=int(len(lista)%2)
        if desenhar:
            for i,intersecao in enumerate(lista):
                fill(*[colorIN,colorOUT][(i+dentro)%2])
                ellipse(intersecao[0],intersecao[1],10,10)
        elif dentro:
            return dentro,ind
    if not desenhar:
        return False,-1
    fill(0,0,0)

def drawRay():
    for i,raio in enumerate(raios):
        fill(255,127)

        if i==(len(raios)-1) and newRay:
            stroke(0)
            raio=raio[:]+[[mouseX,mouseY]]
        else:
            stroke(0)

        
        po,pf=raio
        x0,y0=po
        x1,y1=pf
        dx,dy=x1-x0,y1-y0
        ellipse(x0,y0,10,10)        
        
        x,y=distPoint(x0,y0,x1,y1)
        line(x0,y0,x,y)

       
        line(x0,y0,x1,y1)
        push()
        angulo=atan2(dy,dx)
        translate(x1,y1)
        rotate(angulo+HALF_PI)
        triangle(-7,7,7,7,0,-7/2)
        pop()
    fill(0,0,0)

def mouseClicked(evento):
    global newPolygon,newRay,newVertex,chosenFigure,chosenVertex
    if mouseButton==LEFT:
        if not newRay and not newVertex:
            if newPolygon:
                if evento.getCount()==2:
                    newPolygon=False
                    if len(poligonos[-1])<=2:
                        del poligonos[-1]
                else:
                    poligonos[-1].append([mouseX,mouseY])

            else:
                newPolygon=True
                poligonos.append([[mouseX,mouseY]])

    elif mouseButton==RIGHT:
        if not newPolygon and not newVertex:
            if newRay:
                raios[-1].append([mouseX,mouseY])
                newRay=False

            else:
                newRay=True
                raios.append([[mouseX,mouseY]])


def mouseDragged():
    global newPolygon,newRay,newVertex,chosenFigure,chosenVertex,polygonVertex,DragPolygon,polygonDragged,polygonDragged_Position
    if mouseButton==LEFT:
        if not newRay and not newPolygon:
            if newVertex:
                if polygonVertex:
                    if chosenFigure<=(len(poligonos)-1):
                        poligonos[chosenFigure][chosenVertex]=[mouseX,mouseY]
                else:
                    if chosenFigure<=(len(raios)-1):
                        if chosenVertex==0:
                            x,y=raios[chosenFigure][0]
                            dx,dy=mouseX-x,mouseY-y
                            raios[chosenFigure][0]=[mouseX,mouseY]
                            x2,y2=raios[chosenFigure][1]
                            raios[chosenFigure][1]=[x2+dx,y2+dy]
                        else:
                            raios[chosenFigure][1]=[mouseX,mouseY]

            elif mouseOnVert:
                newVertex=True

    elif mouseButton==RIGHT:
        if DragPolygon:
            dx,dy=[a-b for a,b in zip([mouseX,mouseY],polygonDragged_Position)]
            for i,vertice in enumerate(poligonos[polygonDragged]):
                poligonos[polygonDragged][i]=[vertice[0]+dx,vertice[1]+dy]
            polygonDragged_Position=[mouseX,mouseY]

def mousePressed():
    global newPolygon,newRay,newVertex,chosenFigure,chosenVertex,mouseOnVert,polygonVertex,DragPolygon,polygonDragged,polygonDragged_Position,OnPolygon

    if mouseButton==RIGHT and OnPolygon:
        DragPolygon=True
        

def mouseReleased(): 
    global newPolygon,newRay,newVertex,chosenFigure,chosenVertex,DragPolygon,polygonDragged,polygonDragged_Position,OnPolygon
    if mouseButton==LEFT:
        if newVertex:
            newVertex=False

    elif mouseButton==RIGHT:
        if DragPolygon:
            DragPolygon=False

def mouseMoved():
    global newPolygon,newRay,newVertex,chosenFigure,chosenVertex,mouseOnVert,polygonVertex,DragPolygon,polygonDragged,polygonDragged_Position,OnPolygon
    
    if not newVertex:
        mouseOnVert=False
        for i,poligono in enumerate(poligonos):
            for j,vertice in enumerate(poligono):
                if abs(mouseX-vertice[0])<=15 and abs(mouseY-vertice[1])<=15:
                    chosenFigure=i
                    chosenVertex=j
                    polygonVertex=True
                    mouseOnVert=True
                    break

        if not mouseOnVert:
            for i,raio in enumerate(raios):
                for j,vertice in enumerate(raio):
                    if abs(mouseX-vertice[0])<=15 and abs(mouseY-vertice[1])<=15:
                        chosenFigure=i
                        chosenVertex=j
                        polygonVertex=False
                        mouseOnVert=True
                        break

        if not newRay and not newPolygon:
            a=sqrt(width**2+height**2)
            ponto_distante=[a,a]
            if len(poligonos):
                OnPolygon,polygonDragged=draw_intersections([[mouseX,mouseY],ponto_distante],False)
                if OnPolygon:
                    polygonDragged_Position=[mouseX,mouseY]
