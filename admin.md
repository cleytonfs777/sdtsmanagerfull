 <div class="card">
      <div class="card-body">
        <div class="row d-flex flex-row mb-2 align-items-center">
          <div class="col-md-6 col-6">
            <h5 class="card-title text-success">Projetos de Receita</h5>
          </div>
          <div class="col-md-3 col-6">
            <button class="btn btn-success">Novo</button>
          </div>
          <div class="col-md-3">
            <select
              class="form-select form-select-sm"
              aria-label=".form-select-sm example"
            >
              <option selected>2023</option>
              <option value="1">2022</option>
              <option value="2">2021</option>
              <option value="3">2020</option>
            </select>
          </div>
        </div>
        <div class="row">
          <div class="col-md-3">
            <!-- Card with header and footer -->
            <div class="card">
              <div class="card-header">
                <h5 class="font-weight-bold text-center title-projeto">
                  <a href="{% url 'project' %}?tipo=1"
                    >Expansão DMR Tier III - 2º e 4º COB</a
                  >
                </h5>
              </div>
              <div class="card-body body-projeto">
                <p class="card-text">
                  <span>Descrição:</span> {{ texto|truncatechars:50 }}
                </p>
                <p><span>Data:</span> 15/05/2023</p>
                <p><span>Valor:</span> R$ 1.000.000,00</p>

                <div class="card-footer text-primary">
                  Radio <i class="ri-price-tag-3-fill"></i>
                </div>
              </div>
              <!-- End Card with header and footer -->
            </div>
          </div>
        </div>
      </div>
    </div>