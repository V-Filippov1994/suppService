import React, {useEffect, useState} from "react";
import {api} from "../../api";
import {EQUIPMENT, LOCATIONS_LIST} from "../../api/urls";


const EquipmentForm = () => {
    const [equipmentName, setEquipmentName] = useState("");
    const [locations, setLocations] = useState([]);
    const [selectedLocationIds, setSelectedLocationIds] = useState([]);
    const [success, setSuccess] = useState("");
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchLocations = async () => {
            try {
                const response = await api("get", LOCATIONS_LIST);
                setLocations(response.data);
            } catch {
                setError("Ошибка загрузки локаций");
            }
        };
        void fetchLocations();
    }, []);

    const handleLocationChange = (e) => {
        const options = Array.from(e.target.options);
        const selected = options.filter((o) => o.selected).map((o) => Number(o.value));
        setSelectedLocationIds(selected);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setSuccess("");
        setEquipmentName("");

    if (!equipmentName) {
        setError("Введите имя оборудования");
        return;
    }
    try {
      const payload = {
        name: equipmentName,
        location_ids: selectedLocationIds,
      };
      const response = await api("post", EQUIPMENT, payload);

      if (response.data.error) {
        setError(response.data.error);
      } else {
        setSuccess("Оборудование успешно добавлено");
        setSelectedLocationIds([]);
        setTimeout(() => {
            window.location.reload();
        }, 1000);

      }
    } catch (e) {
      setError("Ошибка при сохранении");
    }
  };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Название оборудования:</label>
                    <input
                      type="text"
                      value={equipmentName}
                      style={{width: '97%'}}
                      onChange={(e) => setEquipmentName(e.target.value)}
                      placeholder="Оборудование 1"
                    />
                </div>

                <div style={{display: 'flex'}}>
                    <select
                      multiple
                      value={selectedLocationIds.map(String)}
                      onChange={handleLocationChange}
                    >
                      {locations.map((loc) => (
                          <option key={loc.id} value={loc.id}>
                              {loc.name}
                          </option>
                      ))}
                    </select>
                </div>

                <button type="submit" className="btn-primary">Сохранить</button>

                {success && (
                    <div style={{
                          color: '#1a5d1a',
                          marginTop: '15px',
                        }}>
                        {success}
                    </div>
                )}
                {error && (
                    <div
                        className="error-message"
                        style={{
                            color: '#e74c3c',
                            marginTop: '15px',
                        }}>
                        {error}
                    </div>
                )}
            </form>
        </div>
    )
}

export default EquipmentForm;