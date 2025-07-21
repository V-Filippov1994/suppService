import React, {useEffect, useState} from "react";
import {api} from "../../api";
import {FABRICS_LIST, LOCATIONS} from "../../api/urls";


const LocationForm = () => {
    const [locationName, setLocationName] = useState('');
    const [fabrics, setFabrics] = useState([]);
    const [selectedFabric, setSelectedFabric] = useState("");
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState('');


    useEffect(() => {
        const fetchAllFabrics = async () => {
            try {
                const response = await api('get', FABRICS_LIST);
                setFabrics(response.data);
            } catch (err) {
                setError(err.response?.data?.detail || 'Ошибка при загрузке данных');
            }
        };
        void fetchAllFabrics();
    }, []);

    const handleChange = (e) => {
        setSelectedFabric(e.target.value);
    };

    const handleSubmit = async (e) => {
        setError(null);
        setLocationName('');
        setSuccess('');
        e.preventDefault();

        if (locationName && selectedFabric) {
            const formData = {'name': locationName, 'fabric_id': selectedFabric}
            const response = await api('post', LOCATIONS, formData);
            if (response.data.error) {
                setError(response.data.error);
            } else {
                setSuccess('Участок успешно добавлен')
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            }
        }
        else {
            setError('Заполните поле');
        }
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>

                <div>
                    <label>Название участка:</label>
                    <input type="text"
                           id="location_name"
                           placeholder="Участок 1"
                           value={locationName}
                           style={{width: '97%'}}
                           onChange={(e) => setLocationName(e.target.value)}/>
                </div>
                <select value={selectedFabric}
                        style={{marginTop: "20px"}}
                        onChange={handleChange}>
                    <option value="">Выберите фабрику</option>
                    {fabrics.map((fabric) => (
                        <option key={fabric.id} value={fabric.id}>
                            {fabric.name}
                        </option>
                    ))}
                </select>

                <button className="btn-primary">Сохранить</button>
            </form>
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
        </div>
    )
}

export default LocationForm;