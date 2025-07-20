import { useEffect, useState } from 'react';
import {EQUIPMENTS_LIST, TREE} from "../../api/urls";
import {api} from "../../api";
import Tree from "../tree/tree";

const EquipmentList = () => {
    const [equipments, setEquipments] = useState([]);
    const [error, setError] = useState(null);
    const [selectedEquipmentsId, setSelectedEquipmentsId] = useState('');
    const [tree, setTree] = useState(null);

    const fetchAllEquipments = async () => {
        try {
            const response = await api('get', EQUIPMENTS_LIST);
            setEquipments(response.data);
        } catch (err) {
            setError(err.response?.data?.detail || 'Ошибка при загрузке данных');
        }
    };

    useEffect(() => {
        void fetchAllEquipments();
    }, []);

    const handleSelectChange = (e) => {
        setSelectedEquipmentsId(e.target.value);
    };

    const handleTreeFabric = async () => {
        const res = await api('get', TREE('equipment', selectedEquipmentsId))
        setTree(res.data)
    }

    return (
        <div>
            <h2>Список Оборудования</h2>
            <div style={{display: 'flex', flexDirection: 'column'}}>
                <button
                    onClick={fetchAllEquipments}
                    type="button">
                  Обновить список
                </button>
                {error && <p style={{ color: 'red' }}>{error}</p>}

               <select
                    value={selectedEquipmentsId}
                    onChange={handleSelectChange}
                >
                    <option value="">Выберите Оборудование</option>
                    {(
                        equipments.map(equipment => (
                            <option key={equipment.id} value={equipment.id}>
                                {equipment.name}
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

export default EquipmentList;
