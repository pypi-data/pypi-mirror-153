import Query from '../../queries/Query.js'
import GraphObjectManager from './GraphObjectManager.js'
import { replaceTemplates } from '../../lib/libaux.js'
import LabelSegmentManager from './LabelSegmentManager.js';

export default class LabelManager extends GraphObjectManager{
    constructor(...args){
        super(...args)
    }


    async load(valueSet){
        var self=this;
        var label=self.graphModelFactory.createLabel(this.type);
        var loadingSubManagers=[];
        self.subManagers.forEach(function(manager){
            let vSet=Object.assign({},valueSet);
            loadingSubManagers.push(manager.load(vSet))
        });   
        
        let res=await Promise.all(loadingSubManagers);

        res.forEach(function(labelSegment){
            label.addSegment(labelSegment);
        })

        label.refreshContent();
        
        return  [label]
    }

    async observe(valueSet,callback,labelProvider){
        var self=this;
        labelProvider.labels.forEach(function(label){
            self.subManagers.forEach(function(manager){
                if(manager instanceof LabelSegmentManager)
                {              
                    label.segments.filter(function(segment){
                        return segment.type==manager.type
                    }).forEach(function(segment){
                        manager.observe(valueSet,segment);
                    })                
                }
            });    
        });
    }

    async unobserve(label)
    {        
        var self=this;   
        self.subManagers.forEach(function(manager){
            if(manager instanceof LabelSegmentManager)
            {              
                label.segments.filter(function(segment){
                    return segment.type==manager.type
                }).forEach(function(segment){
                    manager.unobserve(segment);
                })                
            }
        });         
        
    }




}