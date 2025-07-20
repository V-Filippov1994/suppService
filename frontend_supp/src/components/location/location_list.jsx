import { useEffect, useState } from 'react';
import {LOCATIONS_LIST, TREE} from "../../api/urls";
import {api} from "../../api";
import Tree from "../tree/tree";

const LocationList = () => {
    const [locations, setLocations] = useState([]);
    const [error, setError] = useState(null);
    const [selectedLocationId, setSelectedLocationId] = useState('');
    const [tree, setTree] = useState(null);

    const fetchAllLocations = async () => {
        try {
            const response = await api('get', LOCATIONS_LIST);
            setLocations(response.data);
        } catch (err) {
            setError(err.response?.data?.detail || 'Ошибка при загрузке данных');
        }
    };

    useEffect(() => {
        void fetchAllLocations();
    }, []);

    const handleSelectChange = (e) => {
        setSelectedLocationId(e.target.value);
    };

    const handleTreeFabric = async () => {
        const res = await api('get', TREE('location', selectedLocationId))
        setTree(res.data)
    }
    return (
        <div>
            <h2>Список Участков</h2>
            <div style={{display: 'flex', flexDirection: 'column'}}>
                <button
                    onClick={fetchAllLocations}
                    type="button">
                  Обновить список
                </button>
                {error && <p style={{ color: 'red' }}>{error}</p>}

                <select
                    value={selectedLocationId}
                    onChange={handleSelectChange}
                >
                    <option value="">Выберите Участок</option>
                    {(
                        locations.map(location => (
                            <option key={location.id} value={location.id}>
                                {location.name}
                            </option>
                        ))
                    )}
                </select>

                <button type="button"
                        className="btn-primary"
                        onClick={handleTreeFabric}
                        style={{marginTop: '30px', padding: '10px 0'}}>
                    Показать зависимости
                </button>
            </div>
            {tree ? <Tree data={tree} /> : null}

      </div>
    );
};

export default LocationList;
