import './App.css';
import FabricForm from "./components/fabric/fabric_form";
import FabricsList from "./components/fabric/fabric_list";
import LocationForm from "./components/location/location_form";
import LocationList from "./components/location/location_list";
import EquipmentForm from "./components/equipment/equipment_form";
import EquipmentList from "./components/equipment/equipment_list";

function App() {
  return (
      <div>
        <header>
          <h1>Справочники</h1>
        </header>

      <div className="container">
          <div className="container-item">
              <h2>Фабрики</h2>
              <div>
                  <FabricForm />
              </div>
          </div>

          <div className="container-item">
              <h2>Участки</h2>
              <div>
                  <LocationForm/>
              </div>
          </div>

          <div className="container-item">
              <h2>Оборудование</h2>
              <div>
                  <EquipmentForm/>
              </div>
          </div>

      </div>
      <div>
          <div className='block-supp-list'>
              <FabricsList/>
              <LocationList/>
              <EquipmentList/>
          </div>
      </div>
    </div>
  );
}

export default App;
