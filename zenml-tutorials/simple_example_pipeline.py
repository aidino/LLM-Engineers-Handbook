#!/usr/bin/env python3
"""
Simple ZenML Pipeline - Không cần pandas, tránh lỗi _ctypes

Chạy pipeline này:
1. cd learning-code  
2. poetry run python simple_example_pipeline.py

Pipeline này sử dụng pure Python và built-in libraries
"""

import json
import random
from datetime import datetime
from typing import Any, Dict, List

from zenml import pipeline, step

# ===============================
# STEPS: Các bước xử lý đơn giản
# ===============================

@step
def generate_simple_data() -> Dict[str, Any]:
    """
    🎲 Tạo dữ liệu đơn giản với pure Python
    """
    print("📊 Đang tạo dữ liệu mẫu với pure Python...")
    
    # Set seed cho reproducible results
    random.seed(42)
    
    # Tạo 100 samples
    n_samples = 100
    data = {
        'samples': [],
        'metadata': {
            'count': n_samples,
            'created_at': datetime.now().isoformat(),
            'features': ['value', 'category', 'score']
        }
    }
    
    # Tạo samples
    categories = ['A', 'B', 'C']
    for i in range(n_samples):
        sample = {
            'id': i,
            'value': random.uniform(0, 100),
            'category': random.choice(categories),
            'score': random.randint(1, 10)
        }
        data['samples'].append(sample)
    
    print(f"✅ Đã tạo {n_samples} samples")
    return data

@step
def process_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    🔄 Xử lý dữ liệu đơn giản
    """
    print("🔄 Đang xử lý dữ liệu...")
    
    samples = raw_data['samples']
    
    # Tính thống kê cơ bản
    values = [s['value'] for s in samples]
    scores = [s['score'] for s in samples]
    
    # Tính mean, min, max manually
    value_mean = sum(values) / len(values)
    value_min = min(values)
    value_max = max(values)
    
    score_mean = sum(scores) / len(scores)
    
    # Đếm categories
    category_counts = {}
    for sample in samples:
        cat = sample['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    # Tạo processed data
    processed_data = {
        'original_count': len(samples),
        'statistics': {
            'value_stats': {
                'mean': round(value_mean, 2),
                'min': round(value_min, 2),
                'max': round(value_max, 2),
                'range': round(value_max - value_min, 2)
            },
            'score_stats': {
                'mean': round(score_mean, 2),
                'min': min(scores),
                'max': max(scores)
            },
            'category_distribution': category_counts
        },
        'processed_samples': samples  # Keep original samples
    }
    
    print(f"✅ Đã xử lý {len(samples)} samples")
    print(f"📊 Value mean: {value_mean:.2f}, Score mean: {score_mean:.2f}")
    
    return processed_data

@step
def create_features(processed_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    ⚙️ Tạo features mới
    """
    print("⚙️ Đang tạo features...")
    
    samples = processed_data['processed_samples']
    
    # Tạo features mới cho mỗi sample
    enhanced_samples = []
    for sample in samples:
        enhanced = sample.copy()
        
        # Feature engineering
        enhanced['value_normalized'] = sample['value'] / 100.0  # Normalize to 0-1
        enhanced['score_squared'] = sample['score'] ** 2
        enhanced['value_score_ratio'] = sample['value'] / sample['score'] if sample['score'] > 0 else 0
        
        # Categorical features
        enhanced['is_high_value'] = sample['value'] > 50
        enhanced['is_high_score'] = sample['score'] > 5
        enhanced['category_numeric'] = {'A': 1, 'B': 2, 'C': 3}[sample['category']]
        
        enhanced_samples.append(enhanced)
    
    feature_data = {
        'enhanced_samples': enhanced_samples,
        'feature_info': {
            'original_features': ['value', 'category', 'score'],
            'new_features': ['value_normalized', 'score_squared', 'value_score_ratio', 
                           'is_high_value', 'is_high_score', 'category_numeric'],
            'total_features': 9,
            'sample_count': len(enhanced_samples)
        },
        'statistics': processed_data['statistics']
    }
    
    print(f"✅ Đã tạo {len(feature_data['feature_info']['new_features'])} features mới")
    return feature_data

@step
def simple_model(feature_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    🤖 Model đơn giản - rule-based classifier
    """
    print("🤖 Đang tạo model đơn giản...")
    
    samples = feature_data['enhanced_samples']
    
    # Simple rule-based model: predict based on value and score
    predictions = []
    rules_used = {'high_value_high_score': 0, 'medium': 0, 'low': 0}
    
    for sample in samples:
        # Simple classification rules
        if sample['value'] > 70 and sample['score'] > 7:
            prediction = 'excellent'
            rules_used['high_value_high_score'] += 1
        elif sample['value'] > 40 or sample['score'] > 5:
            prediction = 'good'
            rules_used['medium'] += 1
        else:
            prediction = 'needs_improvement'
            rules_used['low'] += 1
        
        predictions.append({
            'id': sample['id'],
            'prediction': prediction,
            'confidence': min(sample['value'] + sample['score'] * 10, 100) / 100.0
        })
    
    # Calculate prediction distribution
    pred_counts = {}
    confidences = []
    for pred in predictions:
        pred_counts[pred['prediction']] = pred_counts.get(pred['prediction'], 0) + 1
        confidences.append(pred['confidence'])
    
    avg_confidence = sum(confidences) / len(confidences)
    
    model_info = {
        'model_type': 'rule_based_classifier',
        'predictions': predictions,
        'model_stats': {
            'prediction_distribution': pred_counts,
            'average_confidence': round(avg_confidence, 3),
            'rules_usage': rules_used,
            'total_predictions': len(predictions)
        },
        'rules': {
            'excellent': 'value > 70 AND score > 7',
            'good': 'value > 40 OR score > 5',
            'needs_improvement': 'else'
        }
    }
    
    print(f"✅ Model completed. Avg confidence: {avg_confidence:.3f}")
    print(f"📊 Predictions: {pred_counts}")
    
    return model_info

@step
def evaluate_model(model_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    📈 Đánh giá model đơn giản
    """
    print("📈 Đang đánh giá model...")
    
    predictions = model_info['predictions']
    
    # Simple evaluation metrics
    high_confidence_count = sum(1 for p in predictions if p['confidence'] > 0.7)
    medium_confidence_count = sum(1 for p in predictions if 0.4 <= p['confidence'] <= 0.7)
    low_confidence_count = sum(1 for p in predictions if p['confidence'] < 0.4)
    
    confidence_scores = [p['confidence'] for p in predictions]
    avg_confidence = sum(confidence_scores) / len(confidence_scores)
    min_confidence = min(confidence_scores)
    max_confidence = max(confidence_scores)
    
    evaluation_results = {
        'confidence_analysis': {
            'average': round(avg_confidence, 3),
            'min': round(min_confidence, 3),
            'max': round(max_confidence, 3),
            'high_confidence_count': high_confidence_count,
            'medium_confidence_count': medium_confidence_count,
            'low_confidence_count': low_confidence_count
        },
        'prediction_quality': {
            'total_predictions': len(predictions),
            'confidence_distribution': {
                'high': high_confidence_count,
                'medium': medium_confidence_count,
                'low': low_confidence_count
            }
        },
        'model_performance': {
            'reliability_score': round(high_confidence_count / len(predictions), 3),
            'coverage': 1.0,  # Model predicts for all samples
            'model_type': model_info['model_type']
        }
    }
    
    print(f"✅ Evaluation completed. Reliability: {evaluation_results['model_performance']['reliability_score']:.3f}")
    return evaluation_results

@step
def create_summary(
    original_data: Dict[str, Any],
    processed_data: Dict[str, Any], 
    feature_data: Dict[str, Any],
    model_info: Dict[str, Any],
    evaluation: Dict[str, Any]
) -> Dict[str, Any]:
    """
    📋 Tổng hợp kết quả cuối cùng
    """
    print("📋 Đang tạo summary...")
    
    summary = {
        'pipeline_info': {
            'name': 'simple_ml_pipeline',
            'execution_time': datetime.now().isoformat(),
            'status': 'completed_successfully'
        },
        'data_summary': {
            'original_samples': original_data['metadata']['count'],
            'processed_samples': processed_data['original_count'],
            'features_created': len(feature_data['feature_info']['new_features']),
            'total_features': feature_data['feature_info']['total_features']
        },
        'model_summary': {
            'type': model_info['model_type'],
            'predictions_made': model_info['model_stats']['total_predictions'],
            'average_confidence': model_info['model_stats']['average_confidence'],
            'prediction_distribution': model_info['model_stats']['prediction_distribution']
        },
        'evaluation_summary': {
            'reliability_score': evaluation['model_performance']['reliability_score'],
            'high_confidence_predictions': evaluation['confidence_analysis']['high_confidence_count'],
            'average_confidence': evaluation['confidence_analysis']['average'],
        },
        'insights': {
            'most_common_prediction': max(model_info['model_stats']['prediction_distribution'].items(), 
                                        key=lambda x: x[1])[0],
            'confidence_level': 'high' if evaluation['confidence_analysis']['average'] > 0.7 else 
                              'medium' if evaluation['confidence_analysis']['average'] > 0.4 else 'low',
            'data_quality': 'good'  # Simple assessment
        }
    }
    
    print("✅ Pipeline hoàn thành thành công!")
    print(f"📊 Processed {summary['data_summary']['original_samples']} samples")
    print(f"🤖 Model reliability: {summary['evaluation_summary']['reliability_score']:.3f}")
    print(f"🎯 Most common prediction: {summary['insights']['most_common_prediction']}")
    
    return summary

# ===============================
# PIPELINE: Kết hợp các steps
# ===============================

@pipeline
def simple_ml_pipeline() -> Dict[str, Any]:
    """
    🚀 Simple ML Pipeline - Pure Python, không cần pandas
    
    Luồng xử lý:
    1. 📊 Tạo dữ liệu với pure Python
    2. 🔄 Xử lý và tính thống kê  
    3. ⚙️ Feature engineering
    4. 🤖 Rule-based model
    5. 📈 Evaluation
    6. 📋 Summary
    """
    # Pipeline steps
    raw_data = generate_simple_data()
    processed_data = process_data(raw_data)
    feature_data = create_features(processed_data)
    model_info = simple_model(feature_data)
    evaluation = evaluate_model(model_info)
    summary = create_summary(raw_data, processed_data, feature_data, model_info, evaluation)
    
    return summary

# ===============================
# MAIN: Chạy pipeline  
# ===============================

if __name__ == "__main__":
    print("🚀 Bắt đầu chạy Simple ML Pipeline (Pure Python)...")
    print("🔧 Pipeline này không sử dụng pandas để tránh lỗi _ctypes")
    print("=" * 70)
    
    try:
        # Chạy pipeline
        result = simple_ml_pipeline()
        
        print("=" * 70)
        print("🎉 Pipeline hoàn thành thành công!")
        print("\n📊 Kết quả cuối cùng:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        print("\n🔍 Để xem chi tiết pipeline:")
        print("- Web UI: http://127.0.0.1:8237/")
        print("- CLI: poetry run zenml pipeline runs list")
        
        print("\n💡 Tip: Pipeline này sử dụng pure Python, không cần pandas!")
        
    except Exception as e:
        print(f"❌ Lỗi khi chạy pipeline: {e}")
        print(f"🔍 Chi tiết lỗi: {type(e).__name__}")
        print("\n🛠️ Troubleshooting:")
        print("1. Kiểm tra ZenML server: poetry run zenml status")
        print("2. Kiểm tra connection: poetry run zenml login http://127.0.0.1:8237 --api-key --no-verify-ssl")
        print("3. Thử chạy lại: poetry run python simple_example_pipeline.py")
        import traceback
        print(f"\n🚨 Full traceback:\n{traceback.format_exc()}")
        raise 