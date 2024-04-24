let materias= [] ;
const listarMaterias= async (codcarrera)=> {
    try{
        const response = await fetch(`./materiasf/${codcarrera}`);
        const data = await response.json();

        if (data.message==="Success"){
            materias =data.materias;
            
            let opciones=``;
            materias.forEach((materia) => {
            opciones +=`<option value='${materia.id}'>${materia.materia}</option>`;  
            });
            cBoMateria.innerHTML= opciones;
            
        }else{
            alert("Materias no encontradas...");
        }

    }catch (error){
        console.log(error);
    }
};


const cargaInic = async()=>{
    listarMaterias('KTII');
    cBoCarrera.addEventListener("change", (event)=>{
        listarMaterias(event.target.value);
    });
};

window.addEventListener("load", async() =>{
    await cargaInic();
});

