import { useEffect, useState } from 'react';
import {FABRICS_LIST, TREE} from "../../api/urls";
import {api} from "../../api";
import Tree from "../tree/tree";

const FabricsList = () => {
    const [fabrics, setFabrics] = useState([]);
    const [selectedFabricId, setSelectedFabricId] = useState('');
    const [error, setError] = useState(null);
    const [tree, setTree] = useState(null);

    const fetchAllFabrics = async () => {
        try {
            const response = await api('get', FABRICS_LIST);
            setFabrics(response.data);
        } catch (err) {
            setError(err.response?.data?.detail || 'Ошибка при загрузке данных');
        }
    };

    useEffect(() => {
        void fetchAllFabrics();
    }, []);

    const handleSelectChange = (e) => {
        setSelectedFabricId(e.target.value);
    };

    const handleTreeFabric = async () => {
        const res = await api('get', TREE('fabric', selectedFabricId))
        setTree(res.data)
    }
    return (
        <div>
            <h2>Список Фабрик</h2>
            <div style={{display: 'flex', flexDirection: 'column'}}>
                <button
                    onClick={fetchAllFabrics}
                    type="button">
                  Обновить список
                </button>
                {error && <p style={{ color: 'red' }}>{error}</p>}

                <select
                    value={selectedFabricId}
                    onChange={handleSelectChange}
                >
                    <option value="">Выберите фабрику</option>
                    {(
                        fabrics.map(fabric => (
                            <option key={fabric.id} value={fabric.id}>
                                {fabric.name}
                            </option>
                        ))
                    )}
                </select>

                <button type="button"
                        onClick={handleTreeFabric}
                        className="btn-primary"
                        style={{marginTop: '30px', padding: '10px 0'}}>
                    Показать зависимости
                </button>
            </div>
            {tree ? <Tree data={tree} /> : null}
      </div>
    );
};

export default FabricsList;
