<template>
  <div class="container">
    <div class="row">
      <div class="col-6 offset-3">
        <h3 class="text-start">Sintomas</h3>
        <Form :hechos="hechos" @on:click="llenarSintomas" />
      </div>
    </div>
    <div v-if="enfermedad" class="row mt-3">
      <div class="col-6 offset-3 text-start">
        <h3>Diagnostico</h3>
        <p>
          Usted tiene: <span class="text-danger">{{ enfermedad }}</span>
        </p>
        <div class="d-flex mt-3">
          <form>
            <button class="btn btn-danger">Reiniciar</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineAsyncComponent } from "vue";

export default {
  components: {
    Form: defineAsyncComponent(() => import("./Form.vue")),
  },

  data() {
    return {
      hechos: [
        { id: 1, sintomas: "fiebre" },
        { id: 2, sintomas: "tos" },
        { id: 3, sintomas: "malestar" },
        { id: 4, sintomas: "dolor de garganta" },
        { id: 5, enfermedades: "gripa" },
        { id: 6, enfermedades: "faringitis" },
      ],
      reglas: [
        { id: 1, fiebre: "gripa" },
        { id: 2, tos: "gripa" },
        { id: 3, malestar: "gripa" },
        { id: 4, malestar: "faringitis" },
        { id: 5, "dolor de garganta": "faringitis" },
      ],
      sintomas: [],
      agenda: {},
      enfermedad: "",
    };
  },

  methods: {
    llenarSintomas(arr) {
      this.sintomas = [...arr];
    },

    diagnostico() {
      let enfermedades = [];
      for (let enfer in this.agenda) {
        enfermedades = [...enfermedades, enfer];
      }
      let count = 0;
      let diag = "";
      for (let i = 0; i < enfermedades.length; i++) {
        if (this.agenda[enfermedades[i]] > count) {
          count = this.agenda[enfermedades[i]];
          diag = enfermedades[i];
        }
      }
      this.enfermedad = diag;
    },
  },

  watch: {
    sintomas() {
      if (this.sintomas !== []) {
        for (let regla in this.reglas) {
          for (let sintoma of this.sintomas) {
            // console.log(this.reglas[sintoman][sintoma]);
            // console.log(sintoma);
            if (this.agenda[this.reglas[regla][sintoma]]) {
              this.agenda[this.reglas[regla][sintoma]]++;
            } else {
              this.agenda[this.reglas[regla][sintoma]] = 1;
            }
          }
        }
      }
      delete this.agenda["undefined"];
      this.diagnostico();
    },
  },
};
</script>

<style>
</style>